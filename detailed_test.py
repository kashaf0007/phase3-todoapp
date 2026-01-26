import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000/api"

def detailed_test():
    """Detailed test to trace what's happening with user IDs"""
    print("=== Detailed Test with User ID Tracking ===\n")
    
    # Use a specific test user ID
    USER_ID = "test_user_detailed"
    print(f"Using user ID: {USER_ID}")
    
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
            "message": "Add task Test task for detailed analysis",
            "conversation_id": conversation_id
        }
        
        response = requests.post(chat_url, json=payload)
        print(f"Add Task Request Status Code: {response.status_code}")
        if response.status_code == 200:
            add_response = response.json()
            print(f"Add Task Response: {add_response['response']}")
            print(f"Full Add Response: {json.dumps(add_response, indent=2)}")
        else:
            print(f"Add Task Error: {response.text}")
        
        # Now list the tasks using the same user ID
        payload = {
            "message": "List my tasks",
            "conversation_id": conversation_id
        }
        
        response = requests.post(chat_url, json=payload)
        print(f"\nList Tasks Request Status Code: {response.status_code}")
        if response.status_code == 200:
            list_response = response.json()
            print(f"List Tasks Response: {list_response['response']}")
            print(f"Full List Response: {json.dumps(list_response, indent=2)}")
        else:
            print(f"List Tasks Error: {response.text}")
        
        # Get conversation history to verify
        history_url = f"{BASE_URL}/{USER_ID}/conversations/{conversation_id}"
        response = requests.get(history_url)
        print(f"\nGet History Status Code: {response.status_code}")
        if response.status_code == 200:
            history_data = response.json()
            print(f"Messages in conversation: {len(history_data['messages'])}")
            for i, msg in enumerate(history_data['messages']):
                print(f"  {i+1}. [{msg['role']}] {msg['content'][:100]}...")
    else:
        print(f"Error creating conversation: {response.text}")

if __name__ == "__main__":
    detailed_test()