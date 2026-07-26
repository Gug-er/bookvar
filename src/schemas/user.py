from pydantic import BaseModel, ConfigDict, EmailStr


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    
    
class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    super_user: bool = False

    model_config = ConfigDict(
        from_attributes=True
    )