from pydantic import BaseModel

class Task(BaseModel):
    id: int
    project_id: int
    description: str
    is_completed: bool
