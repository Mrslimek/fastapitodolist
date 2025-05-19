import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app
from tests.utils.auth import create_test_access_token


@pytest.mark.parametrize(
    "access_token, expected_status, expected_response",
    [
        (create_test_access_token(username="viktor"), 200, dict),
        (None, 401, None),
        ("invalid_token", 401, None),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_list_user_tasks(access_token, expected_status, expected_response):
    headers = {"Authorization": f"Bearer {access_token}"} if access_token else {}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.get("/tasks", headers=headers)

        assert response.status_code == expected_status, (
            f"Awaited {expected_status}, received {response.status_code}"
        )

        if expected_response is not None:
            assert isinstance(response.json(), expected_response), (
                f"Awaited empty list, returned {response.json()}"
            )
