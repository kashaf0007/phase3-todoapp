import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database.connection import engine
from backend.src.models.conversation import Conversation
from backend.src.models.message import Message
from backend.src.models.task import Task
from sqlmodel import select
from sqlmodel import Session

def check_database():
    """Check if conversations and messages are being stored in the database"""
    print("Checking database for conversations and messages...")

    # Check conversations
    with Session(engine) as session:
        conversations = session.exec(select(Conversation)).all()
        print(f"Found {len(conversations)} conversations in database")

        for conv in conversations:
            print(f"  - ID: {conv.id}, User: {conv.user_id}, Created: {conv.created_at}")

            # Check messages for this conversation
            messages = session.exec(select(Message).where(Message.conversation_id == conv.id)).all()
            print(f"    Messages: {len(messages)}")
            for msg in messages:
                print(f"      - [{msg.role}] {msg.content[:50]}...")

    # Check tasks
    with Session(engine) as session:
        tasks = session.exec(select(Task)).all()
        print(f"\nFound {len(tasks)} tasks in database")
        for task in tasks:
            print(f"  - ID: {task.id}, Title: {task.title}, Completed: {task.completed}, User: {task.user_id}")

if __name__ == "__main__":
    check_database()