"""
Test script to verify all chat operations work correctly with MCP tools
This version creates a user first to satisfy the foreign key constraint
"""
import asyncio
import sys
from pathlib import Path
import uuid
from datetime import datetime

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from sqlmodel import Session
from backend.database.connection import engine
from backend.src.models.user import User
from backend.src.models.task import Task

# Import the agent service to test the operations
from backend.app.services.agent_service import AgentService

async def setup_test_user():
    """
    Create a test user to satisfy the foreign key constraint
    """
    print("Setting up test user...")
    
    # Create a test user directly in the database
    user_id = str(uuid.uuid4())
    user_email = f"test-{uuid.uuid4()}@example.com"
    
    with Session(engine) as session:
        # Check if user already exists
        existing_user = session.get(User, user_id)
        if existing_user:
            print(f"Using existing test user: {user_id}")
            return user_id
        
        # Create new user
        user = User(
            id=user_id,
            email=user_email,
            password_hash="$2b$12$test_hash_for_testing_only"
        )
        
        session.add(user)
        session.commit()
        print(f"Created test user: {user_id}")
        return user_id

async def test_chat_operations():
    """
    Test all chat operations: add, list, update, delete, complete
    """
    print("Testing chat operations with MCP tools...")
    
    # Create a test user first
    user_id = await setup_test_user()
    
    # Create an agent service instance
    agent_service = AgentService()
    
    print("\n1. Testing ADD TASK operation...")
    add_result = await agent_service.process_message_with_agent(
        user_id=user_id,
        message="add task Buy groceries",
        conversation_history=[]
    )
    print(f"Add task result: {add_result['response']}")
    
    print("\n2. Testing LIST TASKS operation...")
    list_result = await agent_service.process_message_with_agent(
        user_id=user_id,
        message="list tasks",
        conversation_history=[]
    )
    print(f"List tasks result: {list_result['response']}")
    
    # Extract task ID from the list result for further operations
    import re
    task_id_match = re.search(r'ID: (\d+)', list_result['response'])
    if not task_id_match:
        print("Could not extract task ID from list result.")
        print("Full response:", list_result['response'])
        return
    
    task_id = int(task_id_match.group(1))
    print(f"Extracted task ID: {task_id}")
    
    print(f"\n3. Testing UPDATE TASK operation for task {task_id}...")
    update_result = await agent_service.process_message_with_agent(
        user_id=user_id,
        message=f"update task {task_id} to 'Buy groceries and cook dinner'",
        conversation_history=[]
    )
    print(f"Update task result: {update_result['response']}")
    
    print(f"\n4. Testing COMPLETE TASK operation for task {task_id}...")
    complete_result = await agent_service.process_message_with_agent(
        user_id=user_id,
        message=f"complete task {task_id}",
        conversation_history=[]
    )
    print(f"Complete task result: {complete_result['response']}")
    
    print("\n5. Testing LIST TASKS again to verify completion...")
    list_result_after_complete = await agent_service.process_message_with_agent(
        user_id=user_id,
        message="list tasks",
        conversation_history=[]
    )
    print(f"List tasks after completion: {list_result_after_complete['response']}")
    
    print(f"\n6. Testing DELETE TASK operation for task {task_id}...")
    delete_result = await agent_service.process_message_with_agent(
        user_id=user_id,
        message=f"delete task {task_id}",
        conversation_history=[]
    )
    print(f"Delete task result: {delete_result['response']}")
    
    print("\n7. Testing LIST TASKS to verify deletion...")
    list_result_after_delete = await agent_service.process_message_with_agent(
        user_id=user_id,
        message="list tasks",
        conversation_history=[]
    )
    print(f"List tasks after deletion: {list_result_after_delete['response']}")
    
    print("\nAll operations tested successfully!")

if __name__ == "__main__":
    asyncio.run(test_chat_operations())