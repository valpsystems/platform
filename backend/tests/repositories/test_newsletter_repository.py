from __future__ import annotations

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants.enums import SubscriptionStatus
from app.repositories.newsletter import NewsletterRepository


@pytest.mark.asyncio
async def test_create_newsletter(db_session: AsyncSession) -> None:
    repo = NewsletterRepository(db_session)
    subscriber = await repo.create(
        email="test@example.com",
        name="Test User",
        is_subscribed=True,
        status=SubscriptionStatus.ACTIVE,
    )
    assert subscriber.id is not None
    assert subscriber.email == "test@example.com"
    assert subscriber.is_subscribed is True


@pytest.mark.asyncio
async def test_unique_email_constraint(db_session: AsyncSession) -> None:
    repo = NewsletterRepository(db_session)
    await repo.create(email="unique@example.com", is_subscribed=True)
    import pytest
    with pytest.raises(Exception):
        await repo.create(email="unique@example.com", is_subscribed=True)


@pytest.mark.asyncio
async def test_find_by_email(db_session: AsyncSession) -> None:
    repo = NewsletterRepository(db_session)
    await repo.create(email="find@example.com", name="Finder", is_subscribed=True)
    result = await repo.first(email="find@example.com")
    assert result is not None
    assert result.name == "Finder"


@pytest.mark.asyncio
async def test_unsubscribe(db_session: AsyncSession) -> None:
    repo = NewsletterRepository(db_session)
    subscriber = await repo.create(
        email="unsub@example.com",
        is_subscribed=True,
        status=SubscriptionStatus.ACTIVE,
    )
    await repo.update(
        subscriber.id,
        is_subscribed=False,
        status=SubscriptionStatus.UNSUBSCRIBED,
    )
    updated = await repo.get(subscriber.id)
    assert updated is not None
    assert updated.is_subscribed is False
    assert updated.status == SubscriptionStatus.UNSUBSCRIBED
