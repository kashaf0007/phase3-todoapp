import requests
import json
import time
import uuid

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

# Test user ID
USER_ID = f"test_user_{uuid.uuid4().hex[:8]}"

def test_scenario_1():
    """Test scenario: Add a task and then list tasks"""
    print("\n--- Scenario 1: Add and List Tasks ---")
    
    # Create a conversation
    url = f"{BASE_URL}/{USER_ID}/conversations"
    response = requests.post(url)
    assert response.status_code == 200, f"Failed to create conversation: {response.text}"
    conversation_id = response.json()['conversation_id']
    print(f"Created conversation: {conversation_id}")

    # Add a task
    url = f"{BASE_URL}/{USER_ID}/chat"
    payload = {
        "message": "Add task Buy groceries",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to add task: {response.text}"
    print(f"Added task response: {response.json()['response']}")

    # List tasks
    payload = {
        "message": "List tasks",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to list tasks: {response.text}"
    print(f"List tasks response: {response.json()['response']}")
    
    return conversation_id

def test_scenario_2():
    """Test scenario: Add multiple tasks and complete one"""
    print("\n--- Scenario 2: Add Multiple Tasks and Complete One ---")
    
    # Create a conversation
    url = f"{BASE_URL}/{USER_ID}/conversations"
    response = requests.post(url)
    assert response.status_code == 200, f"Failed to create conversation: {response.text}"
    conversation_id = response.json()['conversation_id']
    print(f"Created conversation: {conversation_id}")

    # Add first task
    url = f"{BASE_URL}/{USER_ID}/chat"
    payload = {
        "message": "Add task Clean the house",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to add task: {response.text}"
    print(f"Added task response: {response.json()['response']}")

    # Add second task
    payload = {
        "message": "Add task Walk the dog",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to add task: {response.text}"
    print(f"Added task response: {response.json()['response']}")

    # List tasks to see both
    payload = {
        "message": "Show my tasks",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to list tasks: {response.text}"
    print(f"List tasks response: {response.json()['response']}")

    # Complete one task (we'll need to parse the task ID from the previous response)
    # Since we don't know the IDs, let's first get the list again to see the IDs
    payload = {
        "message": "Show my tasks",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to list tasks: {response.text}"
    response_text = response.json()['response']
    print(f"Current tasks: {response_text}")
    
    # Extract task ID from response (this is a simplified extraction)
    # In a real test, we'd need to parse the response properly
    # For now, let's assume we know the task ID is 1
    payload = {
        "message": "Complete task 1",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to complete task: {response.text}"
    print(f"Complete task response: {response.json()['response']}")
    
    return conversation_id

def test_scenario_3():
    """Test scenario: Update and delete tasks"""
    print("\n--- Scenario 3: Update and Delete Tasks ---")
    
    # Create a conversation
    url = f"{BASE_URL}/{USER_ID}/conversations"
    response = requests.post(url)
    assert response.status_code == 200, f"Failed to create conversation: {response.text}"
    conversation_id = response.json()['conversation_id']
    print(f"Created conversation: {conversation_id}")

    # Add a task
    url = f"{BASE_URL}/{USER_ID}/chat"
    payload = {
        "message": "Add task Prepare presentation",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to add task: {response.text}"
    print(f"Added task response: {response.json()['response']}")

    # Update the task
    payload = {
        "message": "Update task 1 to 'Prepare final presentation'",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to update task: {response.text}"
    print(f"Update task response: {response.json()['response']}")

    # Delete the task
    payload = {
        "message": "Delete task 1",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to delete task: {response.text}"
    print(f"Delete task response: {response.json()['response']}")
    
    return conversation_id

def test_scenario_4():
    """Test scenario: General conversation"""
    print("\n--- Scenario 4: General Conversation ---")
    
    # Create a conversation
    url = f"{BASE_URL}/{USER_ID}/conversations"
    response = requests.post(url)
    assert response.status_code == 200, f"Failed to create conversation: {response.text}"
    conversation_id = response.json()['conversation_id']
    print(f"Created conversation: {conversation_id}")

    # Have a general conversation
    url = f"{BASE_URL}/{USER_ID}/chat"
    payload = {
        "message": "Hi there!",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to chat: {response.text}"
    print(f"Response: {response.json()['response']}")

    payload = {
        "message": "What can you help me with?",
        "conversation_id": conversation_id
    }
    response = requests.post(url, json=payload)
    assert response.status_code == 200, f"Failed to chat: {response.text}"
    print(f"Response: {response.json()['response']}")
    
    return conversation_id

if __name__ == "__main__":
    print("Comprehensive Chatbot API Testing...")
    print("="*60)
    
    try:
        # Run all test scenarios
        conv1 = test_scenario_1()
        conv2 = test_scenario_2()
        conv3 = test_scenario_3()
        conv4 = test_scenario_4()
        
        print("\n" + "="*60)
        print("All test scenarios completed successfully!")
        
        print(f"\nUsed conversation IDs:")
        print(f"  Scenario 1: {conv1}")
        print(f"  Scenario 2: {conv2}")
        print(f"  Scenario 3: {conv3}")
        print(f"  Scenario 4: {conv4}")
        
    except Exception as e:
        print(f"\nError during testing: {e}")
        import traceback
        traceback.print_exc()