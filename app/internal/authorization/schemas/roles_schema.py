from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from bson import ObjectId

class RoleBase(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: Optional[str] = None
    permissions: Dict[str, Any] = {}
    
    

class RoleCreate(RoleBase):
    name: str
    description: Optional[str] = None
    permissions: Dict[str, Any] = {}



class RoleUpdate(RoleBase):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None



class RoleInDB(RoleBase):
    id: str = Field(alias="_id")
    permissions: List[str] = []

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {ObjectId: lambda x: str(x)}
    
    

    class Config:
        orm_mode = True


class RoleResponse(BaseModel):
    name: str
    description: Optional[str] = None