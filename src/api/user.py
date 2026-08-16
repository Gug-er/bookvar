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


@router.get("/")
async def get_list_of_users(
    db: DBDep,
    pagination: PaginationDep
):
    users = await db.user.get_all(limit=pagination.per_page, offset=pagination.page-1)
    return users


@router.get("/{user_id}")
async def get_user_by_id(
    db: DBDep,
    user_id: int
) -> UserSchema:
    user = await db.user.get_one_or_none(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}")
async def delete_user(
    db: DBDep,
    user_id: int
):    
    deleted_user = await db.user.delete_filtered(user_id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.commit()
    return {"status": "OK", "detail": "User deleted"}