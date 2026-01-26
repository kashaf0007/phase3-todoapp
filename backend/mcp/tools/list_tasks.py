"""
list_tasks MCP tool implementation
"""
from sqlmodel import Session, select
from ...app.models.task import Task  # Using app models to be consistent
from ...app.services.database import engine  # Using app database connection
from typing import Dict, Any, Optional
import asyncio

async def list_tasks(user_id: str, completed: Optional[bool] = None) -> Dict[str, Any]:
    """
    Retrieves all tasks for a user, optionally filtered by completion status.
    """
    try:
        with Session(engine) as session:
            # Add logging to see what user_id is being used
            print(f"[DEBUG] list_tasks called with user_id: {user_id}")

            # Check all tasks in the database to see what's available
            all_tasks = session.exec(select(Task)).all()
            print(f"[DEBUG] Total tasks in DB: {len(all_tasks)}")

            # Count tasks for this specific user
            user_tasks_count = sum(1 for t in all_tasks if t.user_id == user_id)
            print(f"[DEBUG] Tasks in DB for user {user_id}: {user_tasks_count}")

            # Show all user IDs that exist in the DB
            all_user_ids = set(t.user_id for t in all_tasks)
            print(f"[DEBUG] All user IDs in DB: {all_user_ids}")

            # Build query based on whether we're filtering by completion status
            query = select(Task).where(Task.user_id == user_id)

            if completed is not None:
                query = query.where(Task.completed == completed)

            # Execute the query
            tasks = session.exec(query).all()

            # Log how many tasks were found
            print(f"[DEBUG] Query returned {len(tasks)} tasks for user_id: {user_id}")

            # Format tasks for response
            formatted_tasks = []
            for task in tasks:
                formatted_tasks.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                })

            return {
                "success": True,
                "result": {
                    "tasks": formatted_tasks,
                    "count": len(formatted_tasks)
                }
            }
    except Exception as e:
        print(f"[ERROR] list_tasks error: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "database_error",
                "message": str(e)
            }
        }

# Register the tool
from .registry import register_tool
register_tool("list_tasks")(list_tasks)