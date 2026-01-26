"""
Utility functions for building conversation history for the AI agent
"""
from typing import List, Dict, Any


def build_conversation_history(messages: List) -> List[Dict[str, str]]:
    """
    Convert message objects to the format expected by the AI agent
    """
    result = []
    for msg in messages:
        # Check if it's a Message object (has attributes) or a dict (has get method)
        if hasattr(msg, 'role') and hasattr(msg, 'content'):
            # It's a Message object
            result.append({
                "role": getattr(msg, 'role', 'user'),
                "content": getattr(msg, 'content', '')
            })
        elif hasattr(msg, 'get'):
            # It's a dictionary
            result.append({
                "role": msg.get("role", "user"),
                "content": msg.get("content", "")
            })
        else:
            # Fallback for any other format
            result.append({
                "role": "user",
                "content": str(msg) if msg is not None else ""
            })

    return result