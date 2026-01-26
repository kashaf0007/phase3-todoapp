"""
Chat Service
Handles business logic for chat conversations, message processing and AI agent interaction.
"""

import sys
import os
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Any
from sqlmodel import Session, select

# Add backend root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.src.models.message import Message
from backend.src.models.conversation import Conversation
from backend.mcp.tools.add_task import add_task
from backend.mcp.tools.list_tasks import list_tasks
from backend.mcp.tools.complete_task import complete_task
from backend.mcp.tools.delete_task import delete_task
from backend.mcp.tools.update_task import update_task

# Qwen / OpenAI compatible client (change base_url & api_key as per your provider)
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",          # example: Together AI, OpenRouter, etc.
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Your Qwen model name
MODEL_NAME = "Qwen/Qwen2.5-72B-Instruct"           # ya jo bhi tum use kar rahe ho

# MCP Tools definition (OpenAI-compatible format)
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Create a new todo task for the user",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string", "description": "The authenticated user ID"},
                    "title": {"type": "string", "description": "Short title of the task"},
                    "description": {"type": "string", "description": "Optional detailed description"}
                },
                "required": ["user_id", "title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List user's tasks with optional filtering",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "status": {
                        "type": "string",
                        "enum": ["all", "pending", "completed"],
                        "description": "Filter by status (default: pending)"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task by ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "update_task",
            "description": "Update title or description of an existing task",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "task_id": {"type": "integer"},
                    "title": {"type": "string"},
                    "description": {"type": "string"}
                },
                "required": ["user_id", "task_id"]
            }
        }
    }
]

TOOL_FUNCTION_MAP = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "complete_task": complete_task,
    "delete_task": delete_task,
    "update_task": update_task,
}


import uuid

class ChatService:
    """
    Service class for chat + AI agent logic
    """

    @staticmethod
    def create_conversation(session: Session, user_id: str) -> Conversation:
        """
        Creates a new conversation for a user.
        """
        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=user_id
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    def get_conversation(session: Session, conversation_id: str, user_id: str) -> Conversation:
        """
        Retrieves a specific conversation by its ID for a user.
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation = session.exec(statement).first()
        if not conversation:
            raise ValueError(f"Conversation with ID {conversation_id} not found for user {user_id}")
        return conversation

    @staticmethod
    def create_message(session: Session, user_id: str, conversation_id: str, role: str, content: str) -> Message:
        """
        Creates a new message in a conversation.
        """
        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    def get_messages_for_conversation(session: Session, conversation_id: str, user_id: str, limit: int = 20) -> List[Message]:
        """
        Retrieves messages for a specific conversation.
        """
        # First verify the conversation belongs to the user
        ChatService.get_conversation(session, conversation_id, user_id)

        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.desc()).limit(limit)
        messages = session.exec(statement).all()
        # Reverse to return in chronological order (oldest first)
        return messages[::-1]

    @staticmethod
    def get_system_prompt(user_id: str, history_text: str, current_time: str = "2026-01-26") -> str:
        return f"""You are a helpful Todo AI assistant. Manage tasks using tools only when needed.
Current user ID: {user_id}
Current date/time: {current_time} PKT

Rules:
- Think step-by-step
- Use tools ONLY for task operations
- Always confirm actions in friendly language
- If unclear → ask for clarification
- Respond in JSON format with keys: thought, action, tool_input (if tool), reply

Available tools: add_task, list_tasks, complete_task, delete_task, update_task

Conversation history:
{history_text}

Now respond to the latest user message.
Output ONLY valid JSON.
"""

    @staticmethod
    async def process_message(
        session: Session,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main entry point: process user message → AI → tools → save → return response
        """
        # 1. Get or create conversation
        if not conversation_id:
            conv = ChatService.create_conversation(session, user_id)
            conversation_id = conv.id
        else:
            conv = ChatService.get_conversation(session, conversation_id, user_id)
            if not conv:
                raise ValueError("Conversation not found or access denied")

        # 2. Fetch recent messages (chronological order)
        messages = ChatService.get_messages_for_conversation(session, conversation_id, user_id, limit=20)
        history_text = "\n".join(
            f"{m.role.capitalize()}: {m.content}" for m in messages
        )

        # 3. Save user message
        ChatService.create_message(session, user_id, conversation_id, "user", message)

        # 4. Prepare messages for model
        system_prompt = ChatService.get_system_prompt(user_id, history_text)

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.25,
            max_tokens=1200,
            response_format={"type": "json_object"}   # very important for Qwen stability
        )

        choice = response.choices[0]
        message_content = choice.message.content

        # Parse agent's JSON response
        try:
            agent_reply = json.loads(message_content)
        except json.JSONDecodeError:
            agent_reply = {"thought": "JSON parse failed", "reply": "Sorry, something went wrong on my side. Please try again."}

        final_reply = agent_reply.get("reply", "No reply generated.")
        tool_calls = []

        # 5. Handle tool calls (Qwen may return tool_calls in message.tool_calls)
        if hasattr(choice.message, "tool_calls") and choice.message.tool_calls:
            for tool_call in choice.message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if func_name in TOOL_FUNCTION_MAP:
                    try:
                        # Always inject user_id for security
                        args["user_id"] = user_id
                        result = TOOL_FUNCTION_MAP[func_name](**args)
                        final_reply += f"\n\n**Action result**: {json.dumps(result, indent=2)}"
                        tool_calls.append({
                            "tool": func_name,
                            "input": args,
                            "result": result
                        })
                    except Exception as e:
                        final_reply += f"\n\n**Error**: {str(e)}"
                        tool_calls.append({
                            "tool": func_name,
                            "input": args,
                            "error": str(e)
                        })

        # 6. Save assistant message
        ChatService.create_message(session, user_id, conversation_id, "assistant", final_reply)

        # 7. Update conversation timestamp
        conv.updated_at = datetime.utcnow()
        session.add(conv)
        session.commit()

        return {
            "conversation_id": conversation_id,
            "response": final_reply,
            "tool_calls": tool_calls
        }


# ────────────────────────────────────────────────
#   FastAPI endpoint example (in your router)
# ────────────────────────────────────────────────
# @router.post("/{user_id}/chat")
# async def chat(user_id: str, req: ChatRequest, session: Session = Depends(get_session)):
#     result = await ChatService.process_message(
#         session=session,
#         user_id=user_id,
#         message=req.message,
#         conversation_id=req.conversation_id
#     )
#     return result