from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRequestAdd(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    super_user: bool = False
    
    
class UserAdd(BaseModel):
    email: EmailStr
    hashed_password: str
    first_name: str
    last_name: str
    super_user: bool = False


class UserSchema(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    super_user: bool = False

    model_config = ConfigDict(
        from_attributes=True
    )
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    

class UserHashedPassword(UserSchema):
    hashed_password: str
    
    
class UserPatch(BaseModel):
    email: EmailStr | None = Field(default=None)
    hashed_password: str | None = Field(default=None)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)