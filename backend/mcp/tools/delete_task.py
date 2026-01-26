"""
delete_task MCP tool implementation
"""
from sqlmodel import Session, select
from ...app.models.task import Task  # Using app models to be consistent
from ...app.services.database import engine  # Using app database connection
from typing import Dict, Any
import asyncio

async def delete_task(user_id: str, task_id: str) -> Dict[str, Any]:
    """
    Deletes a task.
    """
    try:
        with Session(engine) as session:
            # Get the task by ID and user ID
            statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
            task = session.exec(statement).first()

            if not task:
                return {
                    "success": False,
                    "error": {
                        "type": "not_found",
                        "message": f"Task with id {task_id} not found for user {user_id}"
                    }
                }

            # Delete the task
            session.delete(task)
            session.commit()

            return {
                "success": True,
                "result": {
                    "message": "Task deleted successfully"
                }
            }
    except Exception as e:
        return {
            "success": False,
            "error": {
                "type": "database_error",
                "message": str(e)
            }
        }

# Register the tool
from .registry import register_tool
register_tool("delete_task")(delete_task)