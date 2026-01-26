"""
Chat API Routes
Handles chat-related API endpoints.
"""

import sys
import os
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session
from typing import Optional
from pydantic import BaseModel

# Use consistent import paths to avoid conflicts
from ...database import get_session
from ...models.conversation import Conversation
from ...models.message import Message

# Import the service from the correct location
# Need to import from the backend root services directory
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
from services.chat_service import ChatService

router = APIRouter(prefix="/api", tags=["Chat"])

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tool_calls: Optional[list] = []
    confirmation: Optional[str] = None
    error: Optional[str] = None

class NewConversationRequest(BaseModel):
    user_id: str

class NewConversationResponse(BaseModel):
    conversation_id: str

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    session: Session = Depends(get_session)
):
    """
    Main chat endpoint for interacting with the AI assistant.
    """
    try:
        # If no conversation ID is provided, create a new conversation
        conversation_id = request.conversation_id
        if not conversation_id:
            conversation = ChatService.create_conversation(session, user_id)
            conversation_id = conversation.id
        else:
            # Verify the conversation belongs to the user
            existing_conversation = ChatService.get_conversation(session, conversation_id, user_id)
            if not existing_conversation:
                raise HTTPException(status_code=404, detail="Conversation not found or access denied")

        # Save the user's message
        user_message = ChatService.create_message(
            session=session,
            user_id=user_id,
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )

        # Integrate with AI agent service to get response
        # Import the agent service to process the message
        from ....app.services.agent_service import AgentService

        # Get conversation history for context
        conversation_history = ChatService.get_messages_for_conversation(
            session=session,
            conversation_id=conversation_id,
            user_id=user_id
        )

        # Build history in the format expected by the agent
        # Convert Message objects to dictionaries
        history_formatted = [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in conversation_history
        ]

        # Process message with agent
        agent_service = AgentService()
        result = await agent_service.process_message_with_agent(
            user_id=user_id,
            message=request.message,
            conversation_history=history_formatted
        )

        ai_response = result["response"]

        # Save the AI's response
        ai_message = ChatService.create_message(
            session=session,
            user_id=user_id,
            conversation_id=conversation_id,
            role="assistant",
            content=ai_response
        )

        # Update conversation timestamp
        conversation = ChatService.get_conversation(session, conversation_id, user_id)
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        session.commit()

        return ChatResponse(
            response=ai_response,
            conversation_id=conversation_id,
            tool_calls=[],
            confirmation=None
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.post("/{user_id}/conversations", response_model=NewConversationResponse)
def create_conversation(
    user_id: str,
    session: Session = Depends(get_session)
):
    """
    Create a new conversation for the user.
    """
    try:
        conversation = ChatService.create_conversation(session, user_id)
        return NewConversationResponse(conversation_id=conversation.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}/conversations/{conversation_id}")
def get_conversation_history(
    user_id: str,
    conversation_id: str,
    session: Session = Depends(get_session)
):
    """
    Get the history of messages for a specific conversation.
    """
    try:
        messages = ChatService.get_messages_for_conversation(session, conversation_id, user_id)
        return {"messages": [message.dict() for message in messages]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))