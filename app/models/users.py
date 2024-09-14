from datetime import datetime
import re
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator

from app.utils.security import hash_password

class User(BaseModel):
    first_name: str
    other_name: str
    last_name: str
    phone:str
    email: EmailStr
    disabled: bool = True
    last_email_update: Optional[datetime] = datetime.now()
    created_at: datetime = datetime.now 
    updated_at: datetime = datetime.now
    
    class Config:
        from_attributes = True

class UserInDB(User):
    hashed_password: str
    


class UserCreate(BaseModel):
    first_name: str
    other_name: str
    last_name: str
    phone:str
    email: EmailStr
    password: str
    last_email_update: Optional[datetime] = datetime.now()
    

