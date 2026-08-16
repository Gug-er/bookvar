from fastapi import APIRouter, HTTPException, Response

from src.dependencies.database import DBDep
from src.schemas.user import UserAdd, UserRequestAdd, UserLogin
from src.services.auth import AuthService

# Handle: change/reset password, change any user data
# Send confirmation email to change or reset password

router = APIRouter(prefix="/auth", tags=["auth"])


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