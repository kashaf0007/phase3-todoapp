#!/usr/bin/env python3
"""Debug script to identify import issues"""

import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

print("Attempting to import the modules that might be causing the issue...")

try:
    print("Importing backend.mcp.server...")
    from backend.mcp.server import get_mcp_server
    print("+ Successfully imported backend.mcp.server")
except ImportError as e:
    print(f"- Failed to import backend.mcp.server: {e}")

try:
    print("Importing backend.app.services.agent_service...")
    from backend.app.services.agent_service import AgentService
    print("+ Successfully imported backend.app.services.agent_service")
except ImportError as e:
    print(f"- Failed to import backend.app.services.agent_service: {e}")

try:
    print("Importing backend.app.main...")
    from backend.app.main import app
    print("+ Successfully imported backend.app.main")
except ImportError as e:
    print(f"- Failed to import backend.app.main: {e}")