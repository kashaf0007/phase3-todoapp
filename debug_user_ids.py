import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.database.connection import engine
from backend.src.models.conversation import Conversation
from backend.src.models.message import Message
from backend.src.models.task import Task
from sqlmodel import select
from sqlmodel import Session

def debug_user_ids():
    """Debug user ID mismatches between conversations, messages, and tasks"""
    print("=== Debugging User ID Mismatches ===\n")
    
    with Session(engine) as session:
        # Get all unique user IDs from tasks
        tasks = session.exec(select(Task)).all()
        print(f"Found {len(tasks)} tasks in database")
        task_user_ids = set(task.user_id for task in tasks)
        print(f"Task user IDs: {task_user_ids}\n")
        
        # Get all unique user IDs from conversations
        conversations = session.exec(select(Conversation)).all()
        print(f"Found {len(conversations)} conversations in database")
        conv_user_ids = set(conv.user_id for conv in conversations)
        print(f"Conversation user IDs: {conv_user_ids}\n")
        
        # Get all unique user IDs from messages
        messages = session.exec(select(Message)).all()
        print(f"Found {len(messages)} messages in database")
        msg_user_ids = set(msg.user_id for msg in messages)
        print(f"Message user IDs: {msg_user_ids}\n")
        
        # Check if there's a mismatch
        print("=== Analysis ===")
        print(f"Task user IDs: {sorted(task_user_ids)}")
        print(f"Conversation user IDs: {sorted(conv_user_ids)}")
        print(f"Message user IDs: {sorted(msg_user_ids)}")
        
        # Find intersection
        common_user_ids = task_user_ids.intersection(conv_user_ids)
        print(f"\nCommon user IDs between tasks and conversations: {common_user_ids}")
        
        # Show tasks for each user
        print("\n=== Tasks by User ===")
        for user_id in task_user_ids:
            user_tasks = [task for task in tasks if task.user_id == user_id]
            print(f"User {user_id}: {len(user_tasks)} tasks")
            for task in user_tasks:
                print(f"  - Task ID {task.id}: '{task.title}' (Completed: {task.completed})")
        
        # Show conversations for each user
        print("\n=== Conversations by User ===")
        for user_id in conv_user_ids:
            user_convs = [conv for conv in conversations if conv.user_id == user_id]
            print(f"User {user_id}: {len(user_convs)} conversations")
            for conv in user_convs:
                conv_msgs = [msg for msg in messages if msg.conversation_id == conv.id]
                print(f"  - Conv {conv.id}: {len(conv_msgs)} messages")

if __name__ == "__main__":
    debug_user_ids()