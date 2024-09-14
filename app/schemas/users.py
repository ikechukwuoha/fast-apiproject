from datetime import datetime
import re
from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, field_validator
from bson import ObjectId
from app.utils.security import hash_password
from app.database.db import users_collection


class User(BaseModel):
    id: Optional[str] = None
    first_name: str
    other_name: str
    last_name: str
    phone: str
    email: EmailStr
    disabled: bool = True
    last_email_update: Optional[datetime] = datetime.now()
    created_at: datetime = datetime.now 
    updated_at: datetime = datetime.now



class UserInDB(User):
    hashed_password: str
    last_email_update: Optional[datetime] = datetime.now()
    
    
    

class UserCreate(BaseModel):
    first_name: str
    other_name: str
    last_name: str
    phone: str
    email: EmailStr
    password:str
    last_email_update: Optional[datetime] = datetime.now()
    
    @field_validator('password', mode="before")
    def validate_password(cls, password):
        # Check if password length is at least 8 characters
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long.')
        
        # Check for uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValueError('Password must contain at least one uppercase letter (A-Z).')

        # Check for number
        if not re.search(r'\d', password):
            raise ValueError('Password must contain at least one number (0-9).')

        # Check for special character
        if not re.search(r'[@$!%*?&]', password):
            raise ValueError('Password must contain at least one special character (@, $, !, %, *, ?, &).')

        return password



# Used For Login
class LoginRequest(BaseModel):
    email: str
    password: str
    

# User Update Schema
class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    disabled: Optional[bool] = None
    last_email_update: Optional[datetime] = datetime.now()


# Function for Response a User Get
class UserResponse(BaseModel):
    first_name: str
    other_name: str
    last_name: str
    phone: str
    email: EmailStr
    disabled: bool
    created_at: datetime=datetime.now()
    updated_at: datetime=datetime.now()
    message: Optional[str] = None 

    class Config:
        from_attributes = True
        

async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    """Retrieve a user by ID asynchronously."""
    try:
        user_id_obj = ObjectId(user_id)  # Convert string ID to ObjectId
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
    
    user = await users_collection.find_one({"_id": user_id_obj})
    if user:
        return UserInDB(**user)
    return None