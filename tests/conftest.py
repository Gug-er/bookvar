import pytest

from src.config import db_settings
from src.db_engine import Base, engine_null_pool
from src.models import *


@pytest.fixture(scope="session", autouse=True)
async def check_conn_mode():
    assert db_settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def async_main(check_conn_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)