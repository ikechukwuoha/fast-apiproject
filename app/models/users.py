from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

from app.utils.security import hash_password

class User(BaseModel):
    id: Optional[str] = None
    first_name: str
    other_name: str
    last_name: str
    phone: str
    email: EmailStr
    is_active: bool = Field(default=False, exclude=True)
    is_admin: bool = Field(default=False, exclude=True)
    is_staff: bool = Field(default=False, exclude=True)
    is_superuser: bool = Field(default=False, exclude=True)
    last_email_update: Optional[datetime] = datetime.now()
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    
    model_config = {
        "from_attributes": True
    }

class UserInDB(User):
    hashed_password: str
