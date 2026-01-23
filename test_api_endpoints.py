"""
Test script to call the API endpoint and verify data insertion
"""
import requests
import json

# Base URL for the API
BASE_URL = "http://127.0.0.1:8000"

def test_create_task_api():
    print("Testing API endpoint to create a task...")
    
    # Data for the new task
    task_data = {
        "user_id": "api_test_user",
        "title": "Task Created via API",
        "description": "This task was created using the POST /tasks/ endpoint"
    }
    
    # Make the API call
    try:
        response = requests.post(f"{BASE_URL}/tasks/", json=task_data)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Task created successfully via API!")
            print(f"Task ID: {result['id']}")
            print(f"Task Title: {result['title']}")
            print(f"User ID: {result['user_id']}")
            print(f"Description: {result['description']}")
            return result
        else:
            print(f"❌ Failed to create task via API. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API. Make sure the FastAPI server is running on http://127.0.0.1:8000")
        print("Run 'python run_api.py' to start the server")
        return None
    except Exception as e:
        print(f"❌ Error calling API: {str(e)}")
        return None

def test_get_tasks_api(user_id):
    print(f"\nTesting API endpoint to get tasks for user: {user_id}")
    
    try:
        response = requests.get(f"{BASE_URL}/tasks/{user_id}")
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Retrieved {len(tasks)} tasks for user {user_id}")
            for task in tasks:
                print(f"  - Task ID: {task['id']}, Title: {task['title']}")
            return tasks
        else:
            print(f"❌ Failed to get tasks via API. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API. Make sure the FastAPI server is running on http://127.0.0.1:8000")
        print("Run 'python run_api.py' to start the server")
        return []
    except Exception as e:
        print(f"❌ Error calling API: {str(e)}")
        return []

if __name__ == "__main__":
    print("Testing API endpoints for task creation and retrieval...\n")
    
    # Test creating a task
    created_task = test_create_task_api()
    
    if created_task:
        # Test retrieving tasks for the user
        test_get_tasks_api(created_task['user_id'])
        
        print("\n✅ API tests completed successfully!")
        print("The task should now be visible in your Neon dashboard.")
    else:
        print("\n❌ API tests failed. Check if the server is running.")