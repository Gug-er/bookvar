from src.utils.db_manager import DBManager
from src.db_engine import async_session_maker
from src.schemas.user import UserRequestAdd, UserAdminAdd
from src.services.auth import AuthService


async def register_admin(
    user: UserRequestAdd
):
    hashed_password = AuthService().hash_password(user.password)
    new_user = UserAdminAdd(
                        email=user.email,
                        hashed_password=hashed_password,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        super_user=True
                )
    async with DBManager(session_factory=async_session_maker) as db:
        registered_user = await db.user.add(new_user)
        await db.commit()
    return registered_user