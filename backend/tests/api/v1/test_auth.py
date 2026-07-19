from __future__ import annotations

import uuid

import pytest
from httpx import AsyncClient


def u(prefix: str = "u") -> tuple[str, str]:
    uid = uuid.uuid4().hex[:8]
    return f"{prefix}_{uid}@example.com", f"{prefix}_{uid}"


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient) -> None:
    email, username = u("reg")
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert "Registration successful" in data["message"]


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    email, username = u("dupe")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username + "2",
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_register_weak_password(client: AsyncClient) -> None:
    email, username = u("weak")
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "short",
            "confirm_password": "short",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_password_mismatch(client: AsyncClient) -> None:
    email, username = u("mismatch")
    response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "DifferentPass456",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient) -> None:
    email, username = u("login")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "TestPass123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert "refresh_token" in data["data"]


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": "nonexistent_" + uuid.uuid4().hex[:8] + "@example.com",
            "password": "WrongPass123",
        },
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient) -> None:
    email, username = u("wrongpw")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "WrongPass123"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_profile_authenticated(client: AsyncClient) -> None:
    email, username = u("profile")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "TestPass123"},
    )
    token = login_resp.json()["data"]["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["email"] == email
    assert data["data"]["username"] == username


@pytest.mark.asyncio
async def test_update_profile(client: AsyncClient) -> None:
    email, username = u("update")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
            "first_name": "Old",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "TestPass123"},
    )
    token = login_resp.json()["data"]["access_token"]

    response = await client.patch(
        "/api/v1/auth/me",
        json={"first_name": "Updated", "phone": "+1234567890"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["first_name"] == "Updated"


@pytest.mark.asyncio
async def test_logout(client: AsyncClient) -> None:
    email, username = u("logout")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "TestPass123"},
    )
    token = login_resp.json()["data"]["access_token"]

    response = await client.post(
        "/api/v1/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True


@pytest.mark.asyncio
async def test_token_refresh(client: AsyncClient) -> None:
    email, username = u("refresh")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "TestPass123"},
    )
    refresh_token = login_resp.json()["data"]["refresh_token"]

    response = await client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data["data"]


@pytest.mark.asyncio
async def test_change_password(client: AsyncClient) -> None:
    email, username = u("changepw")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "TestPass123"},
    )
    token = login_resp.json()["data"]["access_token"]

    response = await client.post(
        "/api/v1/auth/change-password",
        json={
            "current_password": "TestPass123",
            "new_password": "NewPass456",
            "confirm_new_password": "NewPass456",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_change_password_wrong_current(client: AsyncClient) -> None:
    email, username = u("wrongpwch")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    login_resp = await client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": "TestPass123"},
    )
    token = login_resp.json()["data"]["access_token"]

    response = await client.post(
        "/api/v1/auth/change-password",
        json={
            "current_password": "WrongPass123",
            "new_password": "NewPass456",
            "confirm_new_password": "NewPass456",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_forgot_password(client: AsyncClient) -> None:
    email, username = u("forgot")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    response = await client.post(
        "/api/v1/auth/forgot-password",
        json={"email": email},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_forgot_password_nonexistent(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/forgot-password",
        json={"email": "nonexistent_" + uuid.uuid4().hex[:8] + "@example.com"},
    )
    assert response.status_code == 200
    assert "sent" in response.json()["message"].lower()


@pytest.mark.asyncio
async def test_verify_email_invalid_token(client: AsyncClient) -> None:
    response = await client.post(
        "/api/v1/auth/verify-email",
        json={"token": "invalid-token-123"},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_resend_verification(client: AsyncClient) -> None:
    email, username = u("resend")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    response = await client.post(
        "/api/v1/auth/resend-verification",
        json={"email": email},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_expired_token_rejected(client: AsyncClient) -> None:
    fake_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.fake.payload.signature"
    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {fake_token}"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_register_remember_me_login(client: AsyncClient) -> None:
    email, username = u("remember")
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": username,
            "password": "TestPass123",
            "confirm_password": "TestPass123",
        },
    )
    response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": "TestPass123",
            "remember_me": True,
        },
    )
    assert response.status_code == 200
    assert response.json()["data"]["token_type"] == "bearer"
