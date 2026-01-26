"""
Conversation Model
Represents a single conversation thread between user and AI assistant.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class Conversation(SQLModel, table=True):
    """
    Conversation entity for chat sessions.

    Security: ALL queries MUST filter by user_id from authenticated JWT token.
    """
    __tablename__ = "conversations"
    __table_args__ = {"extend_existing": True}

    # Primary key
    id: str = Field(
        primary_key=True,
        description="Unique conversation identifier (UUID or generated string)"
    )

    # Foreign key - User ownership
    user_id: str = Field(
        index=True,
        description="Owner of this conversation (UUID reference to User.id)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Conversation creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        description="Last activity timestamp (auto-updated)"
    )

    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "id": "abc123def456",
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }
        }