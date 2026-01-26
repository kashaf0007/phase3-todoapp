#!/usr/bin/env python3
"""
Final test script to verify the fully fixed chatbot functionality
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
    print("Testing fully fixed chatbot functionality...")
    
    # Initialize the agent service
    agent_service = AgentService()
    
    # Test user ID
    user_id = "final_test_user_456"
    
    # Test various chat commands
    test_messages = [
        "Add task: Buy groceries",
        "Add task - Walk the dog",
        "Create a task Buy milk",
        "List my tasks",
        "Complete task 1",
        "Show my tasks",
        "Delete task 2",
        "List my tasks"
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
        except Exception as e:
            print(f"Error processing message '{message}': {str(e)}")
    
    print("\n--- Final testing completed ---")

if __name__ == "__main__":
    asyncio.run(test_chatbot())