from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.enums import ContactStatus
from app.repositories.contact import ContactRepository


@pytest.mark.asyncio
async def test_create_contact(db_session: AsyncSession) -> None:
    repo = ContactRepository(db_session)
    contact = await repo.create(
        name="John Doe",
        email="john@example.com",
        company="ACME Corp",
        message="Test message for contact form",
        status=ContactStatus.PENDING,
    )
    assert contact.id is not None
    assert contact.name == "John Doe"
    assert contact.email == "john@example.com"
    assert contact.status == ContactStatus.PENDING
    assert contact.is_active is True
    assert contact.is_deleted is False
    assert contact.version == 1


@pytest.mark.asyncio
async def test_get_contact(db_session: AsyncSession) -> None:
    repo = ContactRepository(db_session)
    created = await repo.create(
        name="Jane Doe",
        email="jane@example.com",
        message="Another test message",
    )
    fetched = await repo.get(created.id)
    assert fetched is not None
    assert fetched.name == "Jane Doe"
    assert fetched.email == "jane@example.com"


@pytest.mark.asyncio
async def test_get_nonexistent_contact(db_session: AsyncSession) -> None:
    repo = ContactRepository(db_session)
    result = await repo.get("nonexistent-id")
    assert result is None


@pytest.mark.asyncio
async def test_find_by_email(db_session: AsyncSession) -> None:
    repo = ContactRepository(db_session)
    await repo.create(
        name="Alice",
        email="alice@example.com",
        message="Finding by email test",
    )
    results = await repo.find_by(email="alice@example.com")
    assert len(results) == 1
    assert results[0].name == "Alice"


@pytest.mark.asyncio
async def test_update_contact(db_session: AsyncSession) -> None:
    repo = ContactRepository(db_session)
    contact = await repo.create(
        name="Bob",
        email="bob@example.com",
        message="Update test",
        status=ContactStatus.PENDING,
    )
    updated = await repo.update(contact.id, status=ContactStatus.READ, name="Bob Updated")
    assert updated is not None
    assert updated.name == "Bob Updated"
    assert updated.status == ContactStatus.READ
    assert updated.version == 2


@pytest.mark.asyncio
async def test_soft_delete_contact(db_session: AsyncSession) -> None:
    repo = ContactRepository(db_session)
    contact = await repo.create(
        name="Delete Test",
        email="delete@example.com",
        message="To be deleted",
    )
    assert await repo.get(contact.id) is not None
    deleted = await repo.delete(contact.id)
    assert deleted is True
    assert await repo.get(contact.id) is None


@pytest.mark.asyncio
async def test_restore_contact(db_session: AsyncSession) -> None:
    repo = ContactRepository(db_session)
    contact = await repo.create(
        name="Restore Test",
        email="restore@example.com",
        message="To be restored",
    )
    await repo.delete(contact.id)
    restored = await repo.restore(contact.id)
    assert restored is not None
    assert restored.is_deleted is False
    assert restored.is_active is True


@pytest.mark.asyncio
async def test_pagination(db_session: AsyncSession) -> None:
    repo = ContactRepository(db_session)
    for i in range(25):
        await repo.create(
            name=f"User {i}",
            email=f"user{i}@example.com",
            message=f"Message {i}",
        )
    page1 = await repo.paginate(page=1, page_size=10)
    assert len(page1.items) == 10
    assert page1.total == 25
    assert page1.pages == 3
    assert page1.page == 1

    page2 = await repo.paginate(page=2, page_size=10)
    assert len(page2.items) == 10

    page3 = await repo.paginate(page=3, page_size=10)
    assert len(page3.items) == 5


@pytest.mark.asyncio
async def test_count(db_session: AsyncSession) -> None:
    repo = ContactRepository(db_session)
    assert await repo.count() == 0
    await repo.create(name="Count 1", email="c1@example.com", message="Count test 1")
    await repo.create(name="Count 2", email="c2@example.com", message="Count test 2")
    assert await repo.count() == 2


@pytest.mark.asyncio
async def test_exists(db_session: AsyncSession) -> None:
    repo = ContactRepository(db_session)
    await repo.create(name="Exists Test", email="exists@example.com", message="Exists check")
    assert await repo.exists(email="exists@example.com") is True
    assert await repo.exists(email="noexist@example.com") is False


@pytest.mark.asyncio
async def test_hard_delete(db_session: AsyncSession) -> None:
    repo = ContactRepository(db_session)
    contact = await repo.create(
        name="Hard Delete",
        email="harddelete@example.com",
        message="Hard delete test",
    )
    result = await repo.hard_delete(contact.id)
    assert result is True
    assert await repo.get(contact.id) is None
