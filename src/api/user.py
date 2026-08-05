from fastapi import APIRouter, HTTPException, Request, Response

from src.dependencies.pagination import PaginationDep
from src.dependencies.auth import UserIdDep
from src.dependencies.database import DBDep
from src.schemas.user import UserSchema, UserAdd, UserRequestAdd, UserLogin
from src.services.auth import AuthService


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
async def register_user(
    db: DBDep,
    user: UserRequestAdd
):
    hashed_password = AuthService().hash_password(user.password)
    new_user = UserAdd(
                        email=user.email,
                        hashed_password=hashed_password,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        super_user=user.super_user
                )
    registered_user = await db.user.add(new_user)
    await db.commit()

    return {"status": "OK", "data": registered_user}


@router.post("/login")
async def login_user(
    db: DBDep,
    login_data: UserLogin,
    response: Response
):
    user = await db.user.get_user_by_email(login_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    else:
        if AuthService().verify_password(login_data.password, user.hashed_password):
            jwt_access_token = AuthService().create_access_token({"user_id": user.user_id})
            response.set_cookie(key="jwt_access_token", value=jwt_access_token)
            return {"jwt_access_token": jwt_access_token}
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")


@router.post("/logout")
async def logout(
    response: Response
):
    response.delete_cookie(key="jwt_access_token")
    return {"status": "OK", "detail": "Logged out"}


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
    user = await db.user.get_one_or_none(user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.user.delete_filtered(user_id=user_id)
    await db.commit()
    return {"status": "OK", "detail": "User deleted"}