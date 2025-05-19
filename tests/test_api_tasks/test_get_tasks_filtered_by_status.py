import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.utils.auth import create_test_access_token


@pytest.mark.parametrize(
    "access_token, task_status, expected_status, expected_response",
    [
        (create_test_access_token(username="viktor"), "New", 200, list),
        (create_test_access_token(username="viktor"), "In Progress", 200, list),
        (create_test_access_token(username="viktor"), "Completed", 200, list),
        (create_test_access_token(username="viktor"), "Invalid Status", 422, None),
        (create_test_access_token(username="viktor"), None, 200, list),
        (None, "New", 401, None),
        (None, None, 401, None),
        ("invalid_token", "New", 401, None),
        ("invalid_token", None, 401, None),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_tasks_filtered_by_status(
    access_token, task_status, expected_status, expected_response
):
    headers = (
        {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
        if access_token
        else {"Accept": "application/json"}
    )

    params = {"task_status": task_status} if task_status else {}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tasks/filter/", headers=headers, params=params)

    assert response.status_code == expected_status, (
        f"Expected {expected_status}, got {response.status_code}. Task status: {task_status}"
    )

    if expected_response is not None:
        assert isinstance(response.json(), expected_response), (
            f"Expected response type {expected_response}, got {type(response.json())}. Response data: {response.json()}"
        )
