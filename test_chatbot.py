import requests
import json
import time

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

# Test user ID
USER_ID = "test_user_123"

def test_create_conversation():
    """Test creating a new conversation"""
    url = f"{BASE_URL}/{USER_ID}/conversations"
    response = requests.post(url)
    
    print(f"Create Conversation Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Created Conversation ID: {data['conversation_id']}")
        return data['conversation_id']
    else:
        print(f"Error: {response.text}")
        return None

def test_chat_message(conversation_id):
    """Test sending a chat message"""
    url = f"{BASE_URL}/{USER_ID}/chat"
    payload = {
        "message": "Hello, how can you help me?",
        "conversation_id": conversation_id
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Chat Message Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response']}")
        print(f"Conversation ID: {data['conversation_id']}")
        return data
    else:
        print(f"Error: {response.text}")
        return None

def test_list_tasks(conversation_id):
    """Test listing tasks via chat"""
    url = f"{BASE_URL}/{USER_ID}/chat"
    payload = {
        "message": "Can you list my tasks?",
        "conversation_id": conversation_id
    }
    
    response = requests.post(url, json=payload)
    
    print(f"List Tasks Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response']}")
        return data
    else:
        print(f"Error: {response.text}")
        return None

def test_add_task(conversation_id):
    """Test adding a task via chat"""
    url = f"{BASE_URL}/{USER_ID}/chat"
    payload = {
        "message": "Add a task called 'Buy groceries'",
        "conversation_id": conversation_id
    }
    
    response = requests.post(url, json=payload)
    
    print(f"Add Task Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response']}")
        return data
    else:
        print(f"Error: {response.text}")
        return None

def test_get_conversation_history(conversation_id):
    """Test getting conversation history"""
    url = f"{BASE_URL}/{USER_ID}/conversations/{conversation_id}"
    
    response = requests.get(url)
    
    print(f"Get Conversation History Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Messages count: {len(data['messages'])}")
        for i, msg in enumerate(data['messages']):
            print(f"  {i+1}. [{msg['role']}] {msg['content'][:50]}...")
        return data
    else:
        print(f"Error: {response.text}")
        return None

if __name__ == "__main__":
    print("Testing Chatbot API...")
    print("="*50)
    
    # Create a conversation
    print("\n1. Creating a conversation...")
    conversation_id = test_create_conversation()
    
    if conversation_id:
        print(f"\nUsing conversation ID: {conversation_id}")
        
        # Send initial message
        print("\n2. Sending initial message...")
        test_chat_message(conversation_id)
        
        # Add a task
        print("\n3. Adding a task...")
        test_add_task(conversation_id)
        
        # List tasks
        print("\n4. Listing tasks...")
        test_list_tasks(conversation_id)
        
        # Get conversation history
        print("\n5. Getting conversation history...")
        test_get_conversation_history(conversation_id)
    
    print("\n" + "="*50)
    print("Testing completed!")