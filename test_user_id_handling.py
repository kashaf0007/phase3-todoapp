import requests
import json

# Test to verify user ID handling in the API
def test_user_id_handling():
    print("=== Testing User ID Handling ===\n")
    
    BASE_URL = "http://127.0.0.1:8000/api"
    
    # Test with a unique user ID
    USER_ID = "unique_test_user_12345"
    print(f"Testing with user ID: {USER_ID}")
    
    # Step 1: Create conversation
    conv_url = f"{BASE_URL}/{USER_ID}/conversations"
    conv_response = requests.post(conv_url)
    
    if conv_response.status_code != 200:
        print(f"Failed to create conversation: {conv_response.status_code}, {conv_response.text}")
        return
    
    conversation_id = conv_response.json()["conversation_id"]
    print(f"Created conversation: {conversation_id}")
    
    # Step 2: Add a uniquely identifiable task
    chat_url = f"{BASE_URL}/{USER_ID}/chat"
    add_payload = {
        "message": "Add task Unique Task for user verification test",
        "conversation_id": conversation_id
    }
    
    add_response = requests.post(chat_url, json=add_payload)
    print(f"Add task response: {add_response.status_code}")
    if add_response.status_code == 200:
        print(f"Add response: {add_response.json()['response']}")
    else:
        print(f"Add task failed: {add_response.text}")
    
    # Step 3: List tasks for the same user
    list_payload = {
        "message": "List my tasks",
        "conversation_id": conversation_id
    }
    
    list_response = requests.post(chat_url, json=list_payload)
    print(f"List tasks response: {list_response.status_code}")
    if list_response.status_code == 200:
        print(f"List response: {list_response.json()['response']}")
    else:
        print(f"List tasks failed: {list_response.text}")
    
    # Step 4: Check the database directly for this user ID
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
    
    from backend.database.connection import engine
    from backend.src.models.task import Task
    from sqlmodel import select
    from sqlmodel import Session
    
    with Session(engine) as session:
        # Find tasks for our specific user
        user_tasks = session.exec(select(Task).where(Task.user_id == USER_ID)).all()
        
        print(f"\nTasks found in DB for user {USER_ID}: {len(user_tasks)}")
        for task in user_tasks:
            print(f"  - ID: {task.id}, Title: '{task.title}', Created: {task.created_at}")
    
    # Also check for tasks with our unique content regardless of user
    with Session(engine) as session:
        content_tasks = session.exec(select(Task).where(Task.title.contains("Unique Task"))).all()
        
        print(f"\nTasks with 'Unique Task' in title: {len(content_tasks)}")
        for task in content_tasks:
            print(f"  - ID: {task.id}, User: {task.user_id}, Title: '{task.title}'")

if __name__ == "__main__":
    test_user_id_handling()