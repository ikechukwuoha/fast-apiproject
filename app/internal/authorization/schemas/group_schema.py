from pydantic import BaseModel, Field, field_validator
from typing import Any, Dict, List, Optional
from bson import ObjectId

class GroupBase(BaseModel):
    id: str = Field(alias="_id")
    name: str
    description: Optional[str] = None
    permissions: Dict[str, Any] = {}
    users: Dict[str, Any] = {}
    
   

class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Dict[str, Any] = {}
    users: Dict[str, Any] = {}
    
    
    

class GroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[Dict[str, Any]] = None




class GroupInDB(BaseModel):
    id: str = Field(alias="_id")
    permissions: List[str] = []

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {ObjectId: lambda x: str(x)}
        
        

class GroupResponse(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Dict[str, Any] = {}
    users: Dict[str, Any] = {}