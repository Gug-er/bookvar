from fastapi import APIRouter, HTTPException, Response

from src.dependencies.pagination import PaginationDep
from src.dependencies.auth import UserIdDep
from src.dependencies.database import DBDep
from src.schemas.user import UserSchema, UserAdd, UserRequestAdd, UserLogin
from src.services.auth import AuthService


router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me")
async def get_me(
    db: DBDep,
    user_id: UserIdDep
):
    user = await db.user.get_one_or_none(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}")
async def get_user_by_id(
    db: DBDep,
    user_id: int
) -> UserSchema:
    user = await db.user.get_one_or_none(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


