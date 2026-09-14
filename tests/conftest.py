import pytest
from httpx import AsyncClient, ASGITransport

from main import app

from src.config import db_settings
from src.db_engine import Base, engine_null_pool
from src.models import *


@pytest.fixture(scope="session", autouse=True)
async def check_conn_mode():
    assert db_settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_conn_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
        
@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json = {
                "email" : "test@user.com",
                "password" : "testuserpassword",
                "first_name" : "Test",
                "last_name" : "User"
            }
        )