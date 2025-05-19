import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.utils.auth import create_test_access_token
from app.db.database import get_db
from tests.utils.models import setup_test_task


@pytest.mark.parametrize(
    "access_token, expected_status",
    [
        (create_test_access_token(username="viktor"), 204),
        (None, 401),
        ("invalid_token", 401),
        (create_test_access_token(username="string"), 404),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_delete_task(access_token, expected_status):
    async for db in get_db():
        task_id = await setup_test_task(db)

    headers = (
        {"Authorization": f"Bearer {access_token}", "Accept": "application/json"}
        if access_token
        else {"Accept": "application/json"}
    )

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.delete(f"/tasks/{task_id}", headers=headers)

    assert response.status_code == expected_status, (
        f"Expected {expected_status}, received {response.status_code}. Task ID: {task_id}"
    )
