from src.repos.base import BaseRepository
from src.models.user import UserModel
from src.schemas.user import UserSchema


class UserRepository(BaseRepository):
    model = UserModel
    schema = UserSchema