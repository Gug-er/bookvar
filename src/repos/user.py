from sqlalchemy import select
from pydantic import EmailStr

from src.repos.base import BaseRepository
from src.models.user import UserModel
from src.schemas.user import UserSchema, UserHashedPassword


class UserRepository(BaseRepository):
    model = UserModel
    schema = UserSchema
    
    
    async def get_user_by_email(self, email: EmailStr) -> UserHashedPassword | None:
        query = select(UserHashedPassword).filter_by(email=email)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        
        if model:
            return UserHashedPassword.model_validate(model)
        
        else:
            return None
        