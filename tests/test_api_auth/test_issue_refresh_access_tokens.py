import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.parametrize(
    "username, password, expected_status, expected_response",
    [
        ("viktor", "viktor", 200, dict),
        ("viktor", "viktorrrr", 401, None),
        ("viktor", "vikt", 401, None),
        ("  ", "viktor", 401, None),
        ("nonexistent_user", "any_password", 401, None),
        ("", "correct_password", 401, None),
        ("valid_user", "", 401, None),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_issue_refresh_access_tokens(username, password, expected_status, expected_response):
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    data = {"username": username, "password": password}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/auth/login", headers=headers, data=data)

    assert response.status_code == expected_status, (
        f"Expected {expected_status}, received {response.status_code}. Data sent: {data}"
    )

    if expected_response is not None:
        assert isinstance(response.json(), expected_response), (
            f"Expected response type {expected_response}, got {type(response.json())}. Response data: {response.json()}"
        )
