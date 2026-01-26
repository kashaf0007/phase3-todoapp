"""
Task model with SQLModel
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING, List
from datetime import datetime
import uuid
from .base import BaseSQLModel

if TYPE_CHECKING:
    from .conversation import Conversation  # noqa: F401
    from .message import Message  # noqa: F401

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=10000)
    completed: bool = Field(default=False)
    user_id: str
    tags: Optional[str] = Field(default=None)  # Store tags as JSON string
    category: Optional[str] = Field(default=None, max_length=100)  # Category name

class Task(TaskBase, table=True):
    __tablename__ = "tasks"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)  # Use integer ID to match existing DB schema
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships would go here if needed