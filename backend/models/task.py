"""
Task model definition for the Todo application.
This module defines the Task entity using SQLModel.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """
    Task model representing a user's task in the todo application.
    
    Attributes:
        id: Unique identifier for each task (Primary Key, Auto Increment)
        user_id: Links the task to a specific user (Not Null, Indexed)
        title: Brief description or title of the task (Not Null)
        description: Detailed description of the task (Nullable)
        completed: Indicates whether the task is completed (Default false)
        created_at: Records when the task was created (Auto-generated)
        updated_at: Records when the task was last updated (Auto-updated)
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)