"""
Conversation model with SQLModel
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import uuid
from .base import BaseSQLModel

if TYPE_CHECKING:
    from .message import Message  # noqa: F401
    from .task import Task  # noqa: F401

def generate_uuid():
    return str(uuid.uuid4())

class ConversationBase(SQLModel):
    user_id: str

class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"
    __table_args__ = {"extend_existing": True}

    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships would go here if needed
    # messages: List["Message"] = Relationship(back_populates="conversation")