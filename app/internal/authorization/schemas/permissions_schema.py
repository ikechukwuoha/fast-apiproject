from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId


class PermissionBase(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: Optional[str] = None

    class Config:
        from_attributes = True  # This replaces orm_mode in Pydantic V2
    

class PermissionCreate(PermissionBase):
    name: str
    description: Optional[str] = None


class PermissionUpdate(PermissionBase):
    pass


class PermissionInDB(PermissionBase):
    class Config:
        from_attributes = True  # Ensure compatibility with Pydantic V2
