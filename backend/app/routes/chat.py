"""
Chat endpoint implementation
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session
from ..services.database import get_db_session
from ..schemas.chat import ChatRequest, ChatResponse, ToolCallLog
from ..services.conversation_service import ConversationService
from ..services.message_service import MessageService
from ..services.agent_service import AgentService
from ..utils.auth import require_auth
from ..utils.exceptions import handle_exception
from ..models.conversation import ConversationBase
from ..models.message import MessageBase

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    chat_request: ChatRequest,
    db_session: Session = Depends(get_db_session)
):
    """
    Main chat endpoint at /api/{user_id}/chat
    """
    try:
        # Verify user authentication
        # In a real implementation, we would validate the auth token from headers
        # For now, we'll trust the user_id from the path parameter
        
        # Get or create conversation for this user
        conversation_service = ConversationService(db_session)
        conversations = conversation_service.get_conversations_by_user(user_id)
        
        if conversations:
            # Use the most recent conversation
            conversation = conversations[0]  # Simplified - in reality, you'd want to get the most recent
        else:
            # Create a new conversation
            conversation_data = ConversationBase(user_id=user_id)
            conversation = conversation_service.create_conversation(conversation_data)
        
        # Create message service and save user message
        message_service = MessageService(db_session)
        user_message_data = MessageBase(
            user_id=user_id,
            conversation_id=conversation.id,
            role="user",
            content=chat_request.message
        )
        user_message = message_service.create_message(user_message_data)
        
        # Get conversation history
        conversation_history = message_service.get_messages_by_conversation(conversation.id, user_id)
        
        # Process message with agent
        agent_service = AgentService()
        result = await agent_service.process_message_with_agent(
            user_id=user_id,
            message=chat_request.message,
            conversation_history=[{"role": msg.role, "content": msg.content} for msg in conversation_history]
        )
        
        # Save assistant response
        assistant_message_data = MessageBase(
            user_id=user_id,
            conversation_id=conversation.id,
            role="assistant",
            content=result["response"]
        )
        assistant_message = message_service.create_message(assistant_message_data)
        
        # Return response with tool calls
        return ChatResponse(
            response=result["response"],
            tool_calls=result["tool_calls"],
            conversation_id=conversation.id,
            message_id=assistant_message.id
        )
        
    except Exception as e:
        # Handle application exceptions
        from ..utils.exceptions import BaseAppException
        if isinstance(e, BaseAppException):
            handle_exception(e)
        else:
            # Handle unexpected errors
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"error": {"type": "INTERNAL_ERROR", "message": str(e)}}
            )

            