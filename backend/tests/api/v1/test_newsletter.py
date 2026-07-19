from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_newsletter_success(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/newsletter",
        json={"email": "user@example.com", "name": "Jane"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_newsletter_invalid_email(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/newsletter",
        json={"email": "not-an-email"},
    )
    assert response.status_code == 422
