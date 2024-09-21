from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional



class AdminUser(BaseModel):
    first_name: str
    other_name: Optional[str] = None
    last_name: str
    phone: str
    email: EmailStr
    role: str  # Admin role field 
    permission: Optional[dict] = None 
    super_user: bool = Field(default=False)
    disabled: bool
    last_email_update: Optional[datetime] = datetime.now()
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        from_attributes = True


class AdminUserInDB(AdminUser):
    hashed_password: str