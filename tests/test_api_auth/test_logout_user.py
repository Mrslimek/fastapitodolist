import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app


@pytest.mark.asyncio(loop_scope="session")
async def test_logout_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        data = {"username": "viktor", "password": "viktor"}
        login_response = await client.post("/auth/login", headers=headers, data=data)
        assert login_response.status_code == 200, f"Login failed: {login_response.status_code}"

        logout_headers = {"Authorization": f"Bearer {login_response.json()['access_token']}"}
        logout_response = await client.post("/auth/logout", headers=logout_headers)

        assert logout_response.status_code == 200, f"Logout failed: {logout_response.status_code}"
        assert logout_response.json() == {"status": "success"}, "Unexpected response data"
