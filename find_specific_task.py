import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database.connection import engine
from backend.src.models.task import Task
from sqlmodel import select
from sqlmodel import Session

def find_specific_task():
    """Find a specific task by its content"""
    print("=== Finding Specific Task ===\n")
    
    with Session(engine) as session:
        # Search for tasks containing specific keywords
        tasks = session.exec(select(Task)).all()
        
        print(f"Found {len(tasks)} tasks in database")
        for i, task in enumerate(tasks):
            if 'analysis' in task.title.lower() or 'meeting' in task.title.lower() or 'test' in task.title.lower():
                print(f"{i+1}. ID: {task.id}, User: {task.user_id}")
                print(f"   Title: '{task.title}'")
                print(f"   Description: '{task.description}'")
                print(f"   Completed: {task.completed}")
                print()

if __name__ == "__main__":
    find_specific_task()