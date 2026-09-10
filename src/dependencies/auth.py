from fastapi import Depends, HTTPException, Request
from typing import Annotated

from src.services.auth import AuthService


def get_token(request: Request) -> str:
    token: str = request.cookies.get("jwt_access_token", None)
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    else:
        return token
    
def get_user_id_from_token(token: str = Depends(get_token)) -> int:
    decoded_token = AuthService().decode_access_token(token)
    return decoded_token["user_id"]


def require_admin(token: str = Depends(get_token)) -> bool:
    decoded_token = AuthService().decode_access_token(token)
    if not decoded_token.get("super_user", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    return True


UserIdDep = Annotated[int, Depends(get_user_id_from_token)]
AdminDep = Annotated[bool, Depends(require_admin)]