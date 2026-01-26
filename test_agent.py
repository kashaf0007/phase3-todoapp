#!/usr/bin/env python3
"""Test script to check if the agent service can be instantiated"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("Testing agent service instantiation...")

try:
    from backend.app.services.agent_service import AgentService
    print("+ Successfully imported AgentService")
    
    # Try to instantiate the agent service
    agent_service = AgentService()
    print("+ Successfully instantiated AgentService")
    
    # Try to call a method
    import asyncio
    
    async def test_process():
        result = await agent_service.process_message_with_agent(
            user_id="test_user",
            message="Hello",
            conversation_history=[]
        )
        print(f"+ Successfully processed message: {result}")
    
    asyncio.run(test_process())
    
except Exception as e:
    print(f"- Error: {e}")
    import traceback
    traceback.print_exc()