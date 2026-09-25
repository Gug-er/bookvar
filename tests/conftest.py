import json
import pytest
#from httpx import AsyncClient, ASGITransport

from main import app

from src.config import db_settings
from src.db_engine import Base, engine_null_pool
from src.utils.db_manager import DBManager
from src.models import *
from src.helpers.register_admin import register_admin
from src.db_engine import async_session_maker_null_pool
from src.schemas.user import UserRequestAdd, UserAdd
from src.schemas.book import BookAdd


@pytest.fixture(scope="session", autouse=True)
async def check_conn_mode():
    assert db_settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_conn_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    with open ("tests/mock_books.json", encoding="utf-8") as file_books:
        books_data = json.load(file_books)
    with open ("tests/mock_users.json", encoding="utf-8") as file_users:
        users_data = json.load(file_users)

    books = [BookAdd.model_validate(book) for book in books_data]
    users = [UserAdd.model_validate(user) for user in users_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        await db.book.add_bulk(books)
        await db.user.add_bulk(users)
        await db.commit()


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