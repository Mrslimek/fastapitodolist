import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.utils.auth import create_test_access_token


@pytest.mark.parametrize(
    "body, access_token, expected_status, expected_response",
    [
        (
            {"title": "Task Title"},
            create_test_access_token(username="viktor"),
            201,
            dict,
        ),
        (
            {"title": "Task Title", "description": "Detailed description"},
            create_test_access_token(username="viktor"),
            201,
            dict,
        ),
        (
            {"title": "Task Title", "status": "New"},
            create_test_access_token(username="viktor"),
            201,
            dict,
        ),
        (
            {"title": "Task Title", "status": "In Progress"},
            create_test_access_token(username="viktor"),
            201,
            dict,
        ),
        (
            {"title": "Task Title", "status": "Completed"},
            create_test_access_token(username="viktor"),
            201,
            dict,
        ),
        (
            {"description": "Missing title field"},
            create_test_access_token(username="viktor"),
            422,
            None,
        ),
        (
            {"title": "", "status": "New"},
            create_test_access_token(username="viktor"),
            422,
            None,
        ),
        (
            {"title": "Task Title", "status": "Invalid Status"},
            create_test_access_token(username="viktor"),
            422,
            None,
        ),
        (
            {"title": "Task Title"},
            None,
            401,
            None,
        ),
        (
            {"title": "Task Title"},
            "invalid_token",
            401,
            None,
        ),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_create_task(body, access_token, expected_status, expected_response):
    if access_token:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    else:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/tasks", headers=headers, json=body)

    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, received {response.status_code}. Body sent: {body}"
    )

    if expected_response is not None:
        assert isinstance(response.json(), expected_response), (
            f"Expected response type {expected_response}, returned {type(response.json())}. "
            f"Response data: {response.json()}"
        )
