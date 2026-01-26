"""
Message model with SQLModel
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, Literal, TYPE_CHECKING
from datetime import datetime
import uuid
from .base import BaseSQLModel

if TYPE_CHECKING:
    from .conversation import Conversation  # noqa: F401

def generate_uuid():
    return str(uuid.uuid4())

class MessageBase(SQLModel):
    user_id: str
    conversation_id: str
    role: str
    content: str

class Message(MessageBase, table=True):
    __tablename__ = "messages"
    __table_args__ = {"extend_existing": True}

    id: Optional[str] = Field(default_factory=generate_uuid, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships would go here if needed
    # conversation: "Conversation" = Relationship(back_populates="messages")