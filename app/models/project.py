from pydantic import BaseModel

class Project(BaseModel):
    id: int
    name: str
    client_id: int
