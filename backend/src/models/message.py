"""
Message Model
Represents a single message in a conversation between user and AI assistant.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Message(SQLModel, table=True):
    """
    Message entity for chat conversations.

    Security: ALL queries MUST filter by user_id from authenticated JWT token.
    """
    __tablename__ = "messages"
    __table_args__ = {"extend_existing": True}

    # Primary key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique message identifier (auto-increment)"
    )

    # Foreign key - User ownership
    user_id: str = Field(
        index=True,
        description="Owner of this message (UUID reference to User.id)"
    )

    # Foreign key - Conversation association
    conversation_id: str = Field(
        index=True,
        description="Associated conversation identifier"
    )

    # Message content
    role: str = Field(
        description="Role of message sender ('user' or 'assistant')"
    )
    content: str = Field(
        description="Message content"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Message creation timestamp"
    )

    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "conversation_id": "abc123def456",
                "role": "user",
                "content": "Hello, how can you help me?",
                "created_at": "2025-12-30T10:00:00Z"
            }
        }