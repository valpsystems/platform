from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.enums import ContentStatus
from app.repositories.service import ServiceRepository


@pytest.mark.asyncio
async def test_create_service(db_session: AsyncSession) -> None:
    repo = ServiceRepository(db_session)
    service = await repo.create(
        title="Cloud Engineering",
        slug="cloud-engineering",
        description="Cloud services description",
        icon="Cloud",
        display_order=1,
        is_featured=True,
        status=ContentStatus.PUBLISHED,
    )
    assert service.id is not None
    assert service.title == "Cloud Engineering"
    assert service.slug == "cloud-engineering"
    assert service.is_featured is True
    assert service.display_order == 1


@pytest.mark.asyncio
async def test_find_by_slug(db_session: AsyncSession) -> None:
    repo = ServiceRepository(db_session)
    await repo.create(
        title="DevSecOps",
        slug="devsecops",
        description="Security services",
        status=ContentStatus.PUBLISHED,
    )
    result = await repo.first(slug="devsecops")
    assert result is not None
    assert result.title == "DevSecOps"


@pytest.mark.asyncio
async def test_get_featured_services(db_session: AsyncSession) -> None:
    repo = ServiceRepository(db_session)
    await repo.create(
        title="Service A", slug="service-a",
        is_featured=True, display_order=1, status=ContentStatus.PUBLISHED,
    )
    await repo.create(
        title="Service B", slug="service-b",
        is_featured=False, display_order=2, status=ContentStatus.PUBLISHED,
    )
    await repo.create(
        title="Service C", slug="service-c",
        is_featured=True, display_order=3, status=ContentStatus.PUBLISHED,
    )
    featured = await repo.find_by(is_featured=True)
    assert len(featured) == 2


@pytest.mark.asyncio
async def test_order_by_display_order(db_session: AsyncSession) -> None:
    repo = ServiceRepository(db_session)
    await repo.create(title="Z Service", slug="z-service", display_order=10, status=ContentStatus.PUBLISHED)
    await repo.create(title="A Service", slug="a-service", display_order=1, status=ContentStatus.PUBLISHED)
    services = await repo.get_all(sorts=[("display_order", "asc")])
    assert services[0].display_order == 1
    assert services[0].title == "A Service"
    assert services[-1].display_order == 10
