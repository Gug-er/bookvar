from httpx import AsyncClient, ASGITransport

from main import app

async def test_login_user():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/login",
            json = {
                "email" : "test@user.com",
                "password" : "testuserpassword",
            }
        )