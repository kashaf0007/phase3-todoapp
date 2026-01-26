#!/usr/bin/env python3
"""
Quick test to verify the chatbot is working
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import the agent service from the correct location
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.services.agent_service import AgentService

async def quick_test():
    """Quick test of the chatbot functionality"""
    print("Testing chatbot functionality...")
    
    # Initialize the agent service
    agent_service = AgentService()
    
    # Test user ID
    user_id = "quick_test_user"
    
    # Test adding a task
    print("\n--- Testing add task ---")
    result = await agent_service.process_message_with_agent(
        user_id=user_id,
        message="Add task: Test the chatbot",
        conversation_history=[]
    )
    print(f"Response: {result['response']}")
    
    # Test listing tasks
    print("\n--- Testing list tasks ---")
    result = await agent_service.process_message_with_agent(
        user_id=user_id,
        message="List my tasks",
        conversation_history=[]
    )
    print(f"Response: {result['response']}")
    
    print("\n--- Quick test completed ---")

if __name__ == "__main__":
    asyncio.run(quick_test())