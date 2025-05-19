import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.utils.auth import create_test_access_token
from tests.utils.models import setup_test_task
from app.db.database import get_db


@pytest.mark.parametrize(
    "body, access_token, expected_status, expected_response",
    [
        (
            {"title": "Updated Title"},
            create_test_access_token(username="viktor"),
            200,
            dict,
        ),
        (
            {"description": "New description"},
            create_test_access_token(username="viktor"),
            200,
            dict,
        ),
        (
            {"status": "In Progress"},
            create_test_access_token(username="viktor"),
            200,
            dict,
        ),
        (
            {"title": "Multi-update", "description": "Multi desc", "status": "Completed"},
            create_test_access_token(username="viktor"),
            200,
            dict,
        ),
        (
            {"title": ""},
            create_test_access_token(username="viktor"),
            422,
            None,
        ),
        (
            {"status": "Not a valid status"},
            create_test_access_token(username="viktor"),
            422,
            None,
        ),
        (
            {"title": "No token update"},
            None,
            401,
            None,
        ),
        (
            {"title": "Non-owner update"},
            create_test_access_token(username="string"),
            404,
            None,
        ),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_patch_task(body, access_token, expected_status, expected_response):
    async for db in get_db():
        task_id = await setup_test_task(db=db)
        
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
        response = await client.patch(f"/tasks/{task_id}", headers=headers, json=body)

    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, received {response.status_code}. Request body: {body}"
    )

    if expected_response is not None:
        assert isinstance(response.json(), expected_response), (
            f"Expected response type {expected_response}, got {type(response.json())}. "
            f"Response data: {response.json()}"
        )
