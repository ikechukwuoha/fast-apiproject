from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId




class Permission(BaseModel):
    name: str
    description: Optional[str] = None
    
    

    class Config:
        from_attributes = True
        populate_by_name = True
