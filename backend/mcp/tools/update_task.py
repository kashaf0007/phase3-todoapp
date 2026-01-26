"""
update_task MCP tool implementation
"""
from sqlmodel import Session
from ...app.models.task import Task  # Using app models to be consistent
from ...app.services.database import engine  # Using app database connection
from typing import Dict, Any, Optional
import asyncio

async def update_task(
    user_id: str,
    task_id: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Updates properties of a task.
    """
    try:
        with Session(engine) as session:
            # Get the task by ID
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

            # Update the task with provided fields
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            if completed is not None:
                task.completed = completed

            # Update the timestamp
            from datetime import datetime
            task.updated_at = datetime.utcnow()

            session.add(task)
            session.commit()
            session.refresh(task)

            return {
                "success": True,
                "result": {
                    "message": "Task updated successfully"
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
from sqlmodel import select
register_tool("update_task")(update_task)