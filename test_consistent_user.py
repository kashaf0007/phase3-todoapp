import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

def test_fix():
    """Test with consistent user ID to ensure tasks and conversations match"""
    print("Testing with consistent user ID...")
    
    # Use a consistent user ID
    USER_ID = "consistent_user_123"
    
    # Create a conversation
    url = f"{BASE_URL}/{USER_ID}/conversations"
    response = requests.post(url)
    
    print(f"Create Conversation Status Code: {response.status_code}")
    if response.status_code == 200:
        conversation_data = response.json()
        conversation_id = conversation_data['conversation_id']
        print(f"Created Conversation ID: {conversation_id}")
        
        # Add a task using the chat interface
        chat_url = f"{BASE_URL}/{USER_ID}/chat"
        payload = {
            "message": "Add task Buy milk and bread",
            "conversation_id": conversation_id
        }
        
        response = requests.post(chat_url, json=payload)
        print(f"Add Task Status Code: {response.status_code}")
        if response.status_code == 200:
            add_response = response.json()
            print(f"Add Task Response: {add_response['response']}")
        
        # Now list the tasks using the same conversation
        payload = {
            "message": "List tasks",
            "conversation_id": conversation_id
        }
        
        response = requests.post(chat_url, json=payload)
        print(f"List Tasks Status Code: {response.status_code}")
        if response.status_code == 200:
            list_response = response.json()
            print(f"List Tasks Response: {list_response['response']}")
        
        # Get conversation history to verify
        history_url = f"{BASE_URL}/{USER_ID}/conversations/{conversation_id}"
        response = requests.get(history_url)
        print(f"Get History Status Code: {response.status_code}")
        if response.status_code == 200:
            history_data = response.json()
            print(f"Messages in conversation: {len(history_data['messages'])}")
            for msg in history_data['messages']:
                print(f"  - [{msg['role']}] {msg['content'][:60]}...")
    else:
        print(f"Error creating conversation: {response.text}")

if __name__ == "__main__":
    test_fix()