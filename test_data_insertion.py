"""
Test script to verify data insertion into Neon database
"""
import os
from sqlmodel import Session, select
from backend.database.connection import engine
from backend.models.task import Task
from backend.services.task_service import TaskService

# Make sure the DATABASE_URL is set
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL environment variable is not set!")
else:
    print(f"Using database: {DATABASE_URL}")

def test_data_insertion():
    print("Testing data insertion...")
    
    with Session(engine) as session:
        # Create a test task
        print("Creating a test task...")
        task = TaskService.create_task(
            session=session,
            user_id="test_user_123",
            title="Test Task from Script",
            description="This is a test task to verify data insertion"
        )
        
        print(f"Task created with ID: {task.id}")
        print(f"Task details: {task}")
        
        # Verify the task exists by querying it back
        print("Verifying task exists in database...")
        statement = select(Task).where(Task.id == task.id)
        result = session.exec(statement).first()
        
        if result:
            print(f"Task found in database: {result}")
            print(f"Title: {result.title}")
            print(f"User ID: {result.user_id}")
            print(f"Completed: {result.completed}")
            print(f"Created at: {result.created_at}")
            print(f"Updated at: {result.updated_at}")
        else:
            print("ERROR: Task was not found in the database!")
    
    print("Test completed. Check your Neon dashboard to see if the task appears.")

if __name__ == "__main__":
    test_data_insertion()