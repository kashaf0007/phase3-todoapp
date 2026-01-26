import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database.connection import engine
from backend.src.models.task import Task
from sqlmodel import select
from sqlmodel import Session

def search_for_malformed_task():
    """Search for tasks with the malformed title"""
    print("=== Searching for Malformed Task ===\n")
    
    with Session(engine) as session:
        # Search for tasks with the malformed title pattern
        tasks = session.exec(select(Task)).all()
        
        print(f"Found {len(tasks)} tasks in database")
        for i, task in enumerate(tasks):
            print(f"{i+1}. ID: {task.id}, User: {task.user_id}")
            print(f"   Title: '{task.title}'")
            print(f"   Completed: {task.completed}")
            print(f"   Contains 'Add  Test'?: {'Add  Test' in task.title}")
            print(f"   Contains 'detailed analysis'?: {'detailed analysis' in task.title}")
            print()

if __name__ == "__main__":
    search_for_malformed_task()