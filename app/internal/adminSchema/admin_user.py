import re
from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Dict, Optional
from app.database.db import admin_users_collection
from bson import ObjectId
from app.database.db import admin_users_collection
from app.models.users import UserInDB



class AdminUser(BaseModel):
    id: Optional[str] = None
    first_name: str
    other_name: Optional[str] = None
    last_name: str
    phone: str
    email: EmailStr
    role: str  # Admin role field
    permission: Optional[dict] = None 
    super_user: bool = Field(default=False)
    disabled: bool = True
    last_email_update: Optional[datetime] = datetime.now()
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    
class AdminUserInDB(AdminUser):
    hashed_password: str
    role: str = "superUser"
    last_email_update: Optional[datetime] = datetime.now()





class AdminUserCreate(BaseModel):
    first_name: str
    other_name: Optional[str] = None
    last_name: str
    phone: str
    email: EmailStr
    password: str
    role: str  # For example, 'superadmin', 'moderator', etc.
    disabled: bool =Field(default=False)
    permission: Optional[dict] = None 
    super_user: bool = Field(default=False)
    last_email_update: Optional[datetime] = datetime.now()
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
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
class AdminLoginRequest(BaseModel):
    email: str
    password: str



# User Update Schema
class AdminUserUpdate(BaseModel):
    first_name: Optional[str] = None
    other_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    disabled: Optional[bool] = None
    last_email_update: Optional[datetime] = datetime.now()


class AdminUserResponse(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: str
    disabled: bool
    role: str  # Admin role, e.g., 'superadmin', 'moderator'
    permission: Optional[Dict] = None
    message: Optional[str] = None


    class Config:
        from_attributes = True
        
        
async def get_admin_user_by_id(user_id: str) -> Optional[UserInDB]:
    """Retrieve a user by ID asynchronously."""
    try:
        user_id_obj = ObjectId(user_id)  # Convert string ID to ObjectId
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid user ID format")
    
    user = await admin_users_collection.find_one({"_id": user_id_obj})
    if user:
        return UserInDB(**user)
    return None