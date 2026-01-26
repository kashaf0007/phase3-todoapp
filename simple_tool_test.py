"""
Simple test to check individual tool functionality
"""
import asyncio
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Test the MCP tools directly
from backend.mcp.tools import add_task, list_tasks

async def test_individual_tools():
    print("Testing individual MCP tools...")
    
    user_id = "test-user-123"
    
    # Test adding a task
    print("\n1. Testing add_task tool...")
    add_result = await add_task.add_task(
        user_id=user_id,
        title="Test task",
        description="This is a test task"
    )
    print(f"Add result: {add_result}")
    
    if add_result["success"]:
        # Test listing tasks
        print("\n2. Testing list_tasks tool...")
        list_result = await list_tasks.list_tasks(user_id=user_id)
        print(f"List result: {list_result}")
    else:
        print("Failed to add task, skipping list test")

if __name__ == "__main__":
    asyncio.run(test_individual_tools())