import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database.connection import engine
from backend.src.models.task import Task
from sqlmodel import select
from sqlmodel import Session

def check_latest_tasks():
    """Check the latest tasks added to the database"""
    print("=== Latest Tasks in Database ===\n")
    
    with Session(engine) as session:
        # Get all tasks ordered by creation date (newest first)
        tasks = session.exec(select(Task).order_by(Task.created_at.desc())).all()
        
        print(f"Found {len(tasks)} tasks in database")
        for i, task in enumerate(tasks[:10]):  # Show only the 10 most recent
            print(f"{i+1}. ID: {task.id}, User: {task.user_id}")
            print(f"   Title: '{task.title}'")
            print(f"   Completed: {task.completed}")
            print(f"   Created: {task.created_at}")
            print()

if __name__ == "__main__":
    check_latest_tasks()