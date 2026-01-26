import requests
import json

# Simple test to trigger the API and see debug logs
def simple_trigger():
    print("Triggering API to see debug logs...\n")
    
    BASE_URL = "http://127.0.0.1:8000/api"
    
    # Use a test user ID
    USER_ID = "debug_test_user"
    print(f"Using user ID: {USER_ID}")
    
    # Create a conversation
    conv_url = f"{BASE_URL}/{USER_ID}/conversations"
    conv_response = requests.post(conv_url)
    
    if conv_response.status_code != 200:
        print(f"Failed to create conversation: {conv_response.status_code}")
        return
    
    conversation_id = conv_response.json()["conversation_id"]
    print(f"Created conversation: {conversation_id}")
    
    # Add a task
    chat_url = f"{BASE_URL}/{USER_ID}/chat"
    add_payload = {
        "message": "Add task Debug test task",
        "conversation_id": conversation_id
    }
    
    print("Sending add task request...")
    add_response = requests.post(chat_url, json=add_payload)
    print(f"Add task response: {add_response.status_code}")
    if add_response.status_code == 200:
        print(f"Add response: {add_response.json()['response']}")
    
    # List tasks
    list_payload = {
        "message": "List my tasks",
        "conversation_id": conversation_id
    }
    
    print("Sending list tasks request...")
    list_response = requests.post(chat_url, json=list_payload)
    print(f"List tasks response: {list_response.status_code}")
    if list_response.status_code == 200:
        print(f"List response: {list_response.json()['response']}")

if __name__ == "__main__":
    simple_trigger()