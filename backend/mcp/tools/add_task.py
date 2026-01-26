"""
add_task MCP tool implementation
"""
from sqlmodel import Session, select
from ...app.models.task import Task  # Using app models to be consistent
from ...app.services.database import engine  # Using app database connection
from typing import Dict, Any
import asyncio

async def add_task(user_id: str, title: str, description: str = None) -> Dict[str, Any]:
    """
    Creates a new task for a user.
    """
    # Add logging to see what user_id and title are being used
    print(f"[DEBUG] add_task called with user_id: {user_id}, title: '{title}'")

    # Validate inputs
    if not title or len(title.strip()) == 0:
        print(f"[DEBUG] add_task validation failed: empty title")
        return {
            "success": False,
            "error": {
                "type": "invalid_input",
                "message": "Title is required and must not be empty"
            }
        }

    if description and len(description) > 10000:  # Max length validation
        print(f"[DEBUG] add_task validation failed: description too long")
        return {
            "success": False,
            "error": {
                "type": "invalid_input",
                "message": "Description exceeds maximum length of 10000 characters"
            }
        }

    # Create and save the task in the database
    task_id = None
    try:
        with Session(engine) as session:
            # Create task instance
            task = Task(
                title=title.strip(),
                description=description,
                user_id=user_id,
                completed=False  # Default to not completed
            )
            session.add(task)
            session.commit()
            # Refresh to get the generated ID
            session.refresh(task)
            task_id = task.id
            print(f"[DEBUG] add_task successfully created task ID {task.id} for user {user_id}")

            # Verify the task was actually saved by querying it back
            saved_task = session.get(Task, task.id)
            if saved_task:
                print(f"[DEBUG] Verified task exists in DB: ID {saved_task.id}, User {saved_task.user_id}")
            else:
                print(f"[ERROR] Task {task.id} was not found in DB after commit!")

            return {
                "success": True,
                "result": {
                    "task_id": task.id,
                    "message": "Task created successfully"
                }
            }
    except Exception as e:
        print(f"[ERROR] add_task database error: {str(e)}")
        # If we have a task_id from the exception, try to verify if it was saved
        if task_id:
            try:
                with Session(engine) as session:
                    saved_task = session.get(Task, task_id)
                    if saved_task:
                        print(f"[DEBUG] Task {task_id} exists in DB despite error")
                    else:
                        print(f"[DEBUG] Task {task_id} does not exist in DB after error")
            except Exception as verify_error:
                print(f"[ERROR] Could not verify task existence: {verify_error}")

        return {
            "success": False,
            "error": {
                "type": "database_error",
                "message": str(e)
            }
        }

# Register the tool
from .registry import register_tool
register_tool("add_task")(add_task)