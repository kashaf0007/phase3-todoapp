#!/usr/bin/env python3
"""
Test script to verify the fixed chatbot functionality
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the improved agent service
from improved_agent_service import AgentService

async def test_chatbot():
    """Test the chatbot functionality"""
    print("Testing improved chatbot functionality...")
    
    # Initialize the agent service
    agent_service = AgentService()
    
    # Test user ID
    user_id = "test_user_123"
    
    # Test various chat commands
    test_messages = [
        "Hello, can you help me?",
        "Add a task: Buy groceries",
        "List my tasks",
        "Add task: Complete project proposal",
        "Show my tasks",
        "Complete task 1",
        "Delete task 2",
        "Update task 1 with title 'Buy fresh groceries'"
    ]
    
    for i, message in enumerate(test_messages):
        print(f"\n--- Test {i+1}: {message} ---")
        try:
            result = await agent_service.process_message_with_agent(
                user_id=user_id,
                message=message,
                conversation_history=[]
            )
            print(f"Response: {result['response']}")
            print(f"Success: {result.get('success', 'N/A')}")
        except Exception as e:
            print(f"Error processing message '{message}': {str(e)}")
    
    print("\n--- Testing completed ---")

if __name__ == "__main__":
    asyncio.run(test_chatbot())