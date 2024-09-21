from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from bson import ObjectId

class Role(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Dict[str, Any] = {}


    class Config:
        from_attributes = True
        from_attributes = True  # Replaces `orm_mode`
        populate_by_name = True  # Replaces `allow_population_by_field_name`
