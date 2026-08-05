from fastapi import HTTPException
import jwt, datetime
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext

from src.config import jwt_settings


class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)
    
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(password, hashed_password)
    
    
    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_TIME)
        to_encode |= {"exp": expire}
        encoded_jwt = jwt.encode(to_encode, jwt_settings.JWT_SECRET, algorithm=jwt_settings.JWT_ALGORITHM)
        return encoded_jwt
    

    def decode_access_token(self, jwt_access_token: str) -> dict:
        try:
            return jwt.decode(
                jwt_access_token,
                jwt_settings.JWT_SECRET,
                algorithms=[jwt_settings.JWT_ALGORITHM]
            )
        except jwt.exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Wrong token")