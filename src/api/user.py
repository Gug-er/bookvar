from fastapi import APIRouter

from src.schemas.user import UserAdd, UserRequestAdd
from src.services.auth import hash_password
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
    registered_user = await db.add(new_user)
    await db.commit()

    return {"status": "OK", "data": registered_user}