from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_contact_success(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/contact",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "company": "ACME Corp",
            "message": "I would like to learn more about your platform engineering services.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "John Doe"


@pytest.mark.asyncio
async def test_contact_validation_error(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/contact",
        json={"name": "", "email": "invalid", "message": "short"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_contact_missing_required(client: AsyncClient) -> None:
    response = await client.post("/api/v1/contact", json={})
    assert response.status_code == 422
