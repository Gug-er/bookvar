from fastapi import APIRouter

from src.schemas.user import UserAdd, UserRequestAdd
from src.utils.hashing import hash_password
from src.dependencies.database import DBDep

# registration, authentication, change password or email
router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
async def register_user(
    db: DBDep,
    user: UserRequestAdd
):
    hashed_password = hash_password(user.password)
    new_user = UserAdd(email=user.email, hashed_password=hashed_password)
    is_email_taken = await db.get_one_or_none(new_user.email)
    if is_email_taken:
        return {"error": "Email is already taken"}
    else:
        registered_user = await db.add(new_user)
        await db.commit()

    return {"status": "OK", "data": registered_user}