from __future__ import annotations

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Service is healthy"
    assert data["data"]["status"] == "healthy"
    assert "timestamp" in data


@pytest.mark.asyncio
async def test_health_response_structure(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    data = response.json()
    expected_keys = {"success", "message", "data", "timestamp"}
    assert expected_keys.issubset(data.keys())
    assert isinstance(data["data"], dict)
    assert data["data"]["version"] == "1.0.0"
