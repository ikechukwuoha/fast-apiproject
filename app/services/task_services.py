from app.models.task import Task

def get_task(task_id: int) -> Task:
    # Placeholder for actual database call
    return Task(id=task_id, project_id=1, description="Test Task", is_completed=False)
