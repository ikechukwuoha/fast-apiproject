from app.models.project import Project

def get_project(project_id: int) -> Project:
    # Placeholder for actual database call
    return Project(id=project_id, name="Test Project", client_id=1)
