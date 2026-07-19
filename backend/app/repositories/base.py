from __future__ import annotations

import operator
from collections.abc import Sequence
from functools import reduce
from typing import Any, TypeVar

from sqlalchemy import Select, UnaryExpression, asc, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class PaginatedResult[ModelType: Base]:
    def __init__(
        self,
        items: Sequence[ModelType],
        total: int,
        page: int,
        page_size: int,
    ):
        self.items = items
        self.total = total
        self.page = page
        self.page_size = page_size
        self.pages = (total + page_size - 1) // page_size if page_size > 0 else 0


class BaseRepository[ModelType: Base]:
    def __init__(self, model: type[ModelType], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    def _not_deleted(self) -> Any:
        return self.model.is_deleted.is_(False)

    def _base_query(self) -> Select:
        return select(self.model).where(self._not_deleted())

    async def create(self, **kwargs: Any) -> ModelType:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def bulk_create(self, items: list[dict[str, Any]]) -> list[ModelType]:
        instances = [self.model(**item) for item in items]
        self.session.add_all(instances)
        await self.session.flush()
        for instance in instances:
            await self.session.refresh(instance)
        return instances

    async def get(self, id: str) -> ModelType | None:
        result = await self.session.execute(
            self._base_query().where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_ids(self, ids: list[str]) -> Sequence[ModelType]:
        result = await self.session.execute(
            self._base_query().where(self.model.id.in_(ids))
        )
        return result.scalars().all()

    async def get_active(self, id: str) -> ModelType | None:
        result = await self.session.execute(
            self._base_query().where(
                self.model.id == id,
                self.model.is_active.is_(True),
            )
        )
        return result.scalar_one_or_none()

    async def first(self, **filters: Any) -> ModelType | None:
        stmt = self._base_query()
        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        result = await self.session.execute(stmt.limit(1))
        return result.scalar_one_or_none()

    async def find_by(self, **filters: Any) -> Sequence[ModelType]:
        stmt = self._base_query()
        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        sorts: list[tuple[str, str]] | None = None,
    ) -> Sequence[ModelType]:
        stmt = self._base_query()
        stmt = self._apply_sorting(stmt, sorts)
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def paginate(
        self,
        page: int = 1,
        page_size: int = 20,
        sorts: list[tuple[str, str]] | None = None,
        **filters: Any,
    ) -> PaginatedResult[ModelType]:
        base_stmt = self._base_query()
        for key, value in filters.items():
            base_stmt = base_stmt.where(getattr(self.model, key) == value)

        count_stmt = select(func.count()).select_from(base_stmt.subquery())
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar() or 0

        offset = (page - 1) * page_size
        stmt = base_stmt
        stmt = self._apply_sorting(stmt, sorts)
        stmt = stmt.offset(offset).limit(page_size)
        result = await self.session.execute(stmt)
        items = result.scalars().all()

        return PaginatedResult(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        )

    async def update(self, id: str, **kwargs: Any) -> ModelType | None:
        instance = await self.get(id)
        if instance is None:
            return None
        for key, value in kwargs.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        instance.version += 1
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id: str) -> bool:
        instance = await self.get(id)
        if instance is None:
            return False
        instance.soft_delete()
        await self.session.flush()
        return True

    async def hard_delete(self, id: str) -> bool:
        instance = await self.session.get(self.model, id)
        if instance is None:
            return False
        await self.session.delete(instance)
        await self.session.flush()
        return True

    async def restore(self, id: str) -> ModelType | None:
        result = await self.session.execute(
            select(self.model).where(
                self.model.id == id,
                self.model.is_deleted.is_(True),
            )
        )
        instance = result.scalar_one_or_none()
        if instance is None:
            return None
        instance.restore()
        instance.version += 1
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def exists(self, **kwargs: Any) -> bool:
        stmt = select(func.count()).select_from(self.model).where(self._not_deleted())
        for key, value in kwargs.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        result = await self.session.execute(stmt)
        count = result.scalar()
        return count is not None and count > 0

    async def count(self, **filters: Any) -> int:
        stmt = select(func.count()).select_from(self.model).where(self._not_deleted())
        for key, value in filters.items():
            stmt = stmt.where(getattr(self.model, key) == value)
        result = await self.session.execute(stmt)
        count = result.scalar()
        return count or 0

    async def search(
        self,
        query: str,
        fields: list[str],
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[ModelType]:
        stmt = self._base_query()
        if query and fields:
            conditions = [
                getattr(self.model, field).ilike(f"%{query}%")
                for field in fields
                if hasattr(self.model, field)
            ]
            if conditions:
                stmt = stmt.where(reduce(operator.or_, conditions))
        stmt = stmt.offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    def _apply_sorting(
        self,
        stmt: Select,
        sorts: list[tuple[str, str]] | None,
    ) -> Select:
        if not sorts:
            return stmt.order_by(self.model.created_at.desc())
        order_clauses: list[UnaryExpression] = []
        for field, direction in sorts:
            if hasattr(self.model, field):
                column = getattr(self.model, field)
                order_clauses.append(
                    desc(column) if direction.lower() == "desc" else asc(column)
                )
        if order_clauses:
            stmt = stmt.order_by(*order_clauses)
        return stmt
