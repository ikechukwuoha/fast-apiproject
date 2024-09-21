from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional
from bson import ObjectId

class Group(BaseModel):
    name: str
    description: Optional[str] = None
    permissions: Dict[str, str] = {}
    users: Dict[str, Any] = {}  # Object of user IDs (as strings)

    class Config:
        json_encoders = {
            ObjectId: str  # Ensure ObjectId is converted to string
        }
        arbitrary_types_allowed = True  # Allow non-standard types like ObjectId