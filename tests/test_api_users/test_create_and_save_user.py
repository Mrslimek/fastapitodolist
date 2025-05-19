import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.utils.models import random_string


@pytest.mark.parametrize(
    "body, expected_status, expected_response",
    [
        ({"username": random_string(10), "first_name": "John", "password": "secure123"}, 201, dict),
        (
            {"username": "Mr.", "first_name": "Doe", "last_name": "Smith", "password": "secure123"},
            409,
            dict,
        ),
        ({"username": random_string(10), "first_name": "Jane", "password": "short"}, 422, None),
        ({"username": random_string(10), "first_name": "", "password": "secure123"}, 422, None),
        ({"first_name": "Alice", "password": "secure123"}, 422, None),
        ({"username": random_string(10), "password": "secure123"}, 422, None),
        ({"username": random_string(10), "first_name": "Robert"}, 422, None),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_create_and_save_user(body, expected_status, expected_response):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/users/register", headers=headers, json=body)

    assert response.status_code == expected_status, (
        f"Expected {expected_status}, received {response.status_code}. Body sent: {body}"
    )

    if expected_response is not None:
        assert isinstance(response.json(), expected_response), (
            f"Expected response type {expected_response}, got {type(response.json())}. Response data: {response.json()}"
        )
