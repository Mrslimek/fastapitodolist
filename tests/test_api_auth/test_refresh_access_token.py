import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from tests.utils.auth import create_test_refresh_token
from app.config import settings


@pytest.mark.parametrize(
    "refresh_token, expected_status, expected_response",
    [
        (None, 401, None),
        ("invalid_token", 401, None),
        (
            create_test_refresh_token(
                username="viktor",
                token_type=settings.REFRESH_TOKEN_TYPE,
                expire_timedelta=settings.REFRESH_TOKEN_EXPIRE_DAYS,
                private_key=settings.PRIVATE_KEY_PATH.read_text(),
                algorithm=settings.ALGORITHM,
                expired=True,
            ),
            401,
            None,
        ),
        (
            create_test_refresh_token(
                username="viktor",
                token_type=settings.ACCESS_TOKEN_TYPE,
                expire_timedelta=settings.REFRESH_TOKEN_EXPIRE_DAYS,
                private_key=settings.PRIVATE_KEY_PATH.read_text(),
                algorithm=settings.ALGORITHM,
                expired=False,
            ),
            401,
            None,
        ),
        (
            create_test_refresh_token(
                username="ghost_user",
                token_type=settings.REFRESH_TOKEN_TYPE,
                expire_timedelta=settings.REFRESH_TOKEN_EXPIRE_DAYS,
                private_key=settings.PRIVATE_KEY_PATH.read_text(),
                algorithm=settings.ALGORITHM,
                expired=False,
            ),
            401,
            None,
        ),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_refresh_access_token(refresh_token, expected_status, expected_response):
    """
    We can't mark cookie here as httponly, so server won't accept it,
    so we only can test server's reaction to the wrong refresh token.
    For testing correct reaction to correct refresh token better using Postman
    """

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        client.cookies.set("refresh", refresh_token, domain="localhost")
        response = await client.post("/auth/refresh")

    assert response.status_code == expected_status, (
        f"Expected {expected_status}, received {response.status_code}. Token: {refresh_token}"
    )

    if expected_response is not None:
        assert isinstance(response.json(), expected_response), (
            f"Expected response type {expected_response}, got {type(response.json())}. Response data: {response.json()}"
        )
