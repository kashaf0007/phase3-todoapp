"""
Task Model
Represents a single todo item belonging to exactly one user.
Supports five basic operations: create, read, update, delete, mark complete.
"""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.schema import CreateTable


class Task(SQLModel, table=True):
    """
    Task entity for todo list management.

    Security: ALL queries MUST filter by user_id from authenticated JWT token.
    """
    __tablename__ = "tasks"
    __table_args__ = {"extend_existing": True}

    # Primary key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Unique task identifier (auto-increment)"
    )

    # Foreign key - User ownership
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        description="Owner of this task (UUID reference to User.id)"
    )

    # Task content
    title: str = Field(
        max_length=255,
        description="Task title (required, 1-255 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional task description (0-2000 characters)"
    )

    # Task status
    completed: bool = Field(
        default=False,
        description="Completion status (False = incomplete, True = complete)"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        description="Last modification timestamp (auto-updated)"
    )

    class Config:
        """Pydantic configuration"""
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }
        }
