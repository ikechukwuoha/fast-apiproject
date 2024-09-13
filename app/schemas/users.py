from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.utils.security import hash_password


class User(BaseModel):
    first_name: str
    other_name: str
    last_name: str
    phone: str
    email: EmailStr
    disabled: bool = True
    created_at: datetime = datetime.now 
    updated_at: datetime = datetime.now

class UserInDB(User):
    hashed_password: hash_password

class UserCreate(BaseModel):
    first_name: str
    other_name: str
    last_name: str
    phone: str
    email: EmailStr
    password:str


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    first_name: str
    other_name: str
    last_name: str
    phone: str
    email: EmailStr
    disabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
