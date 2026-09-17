import pytest
from httpx import AsyncClient, ASGITransport

from main import app

from src.config import db_settings
from src.db_engine import Base, engine_null_pool
from src.models import *
from src.helpers.register_admin import register_admin
from src.schemas.user import UserRequestAdd


@pytest.fixture(scope="session", autouse=True)
async def check_conn_mode():
    assert db_settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_conn_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
        
@pytest.fixture(scope="session", autouse=True)
async def register_test_user(setup_database):
    test_user_data = UserRequestAdd(
        email = "test@user.com",
        password = "testuserpassword",
        first_name = "Test",
        last_name = "User"
    )
    registered_user = await register_admin(user = test_user_data)
    assert registered_user