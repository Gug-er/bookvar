from fastapi import APIRouter, HTTPException, Response

from src.schemas.user import UserAdd, UserRequestAdd, UserLogin
from src.services.auth import AuthService
from src.dependencies.database import DBDep

# registration, authentication, change password or email
router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register")
async def register_user(
    db: DBDep,
    user: UserRequestAdd
):
    hashed_password = AuthService().hash_password(user.password)
    new_user = UserAdd(email=user.email, hashed_password=hashed_password)
    registered_user = await db.add(new_user)
    await db.commit()

    return {"status": "OK", "data": registered_user}


@router.post("/login")
async def login_user(
    db: DBDep,
    login_data: UserLogin,
    response: Response
):
    user = await db.get_user_by_email(login_data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    else:
        if AuthService().verify_password(login_data.password, user.hashed_password):
            access_token = AuthService().create_access_token(user.id)
            response.set_cookie(key="jwt_access_token", value=access_token)
            return {"access_token": access_token}
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
            