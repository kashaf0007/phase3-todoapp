# Data Model: Neon PostgreSQL Setup & Table Visibility

## 1. Task Entity

### Entity Name: Task
**Description**: Represents a user's task in the todo application

### Fields:
- **id**: integer (Primary Key, Auto Increment)
  - Purpose: Unique identifier for each task
  - Constraints: Primary key, auto-increment
- **user_id**: string (Not Null, Indexed)
  - Purpose: Links the task to a specific user
  - Constraints: Not null, indexed for performance
- **title**: string (Not Null)
  - Purpose: Brief description or title of the task
  - Constraints: Not null
- **description**: text (Nullable)
  - Purpose: Detailed description of the task
  - Constraints: Optional field
- **completed**: boolean (Default false)
  - Purpose: Indicates whether the task is completed
  - Constraints: Boolean with default value of false
- **created_at**: timestamp (Auto-generated)
  - Purpose: Records when the task was created
  - Constraints: Automatically set when record is created
- **updated_at**: timestamp (Auto-updated)
  - Purpose: Records when the task was last updated
  - Constraints: Automatically updated when record is modified

### Relationships:
- **Belongs to**: User (via user_id foreign key)
  - Each task is associated with exactly one user
  - Enforces user isolation as required by the constitution

### Validation Rules:
- title must not be empty
- user_id must correspond to an existing user
- created_at and updated_at are automatically managed by the database layer
- completed field defaults to false when not specified

## 2. Database Schema

### Table: tasks
**Purpose**: Stores all user tasks with proper isolation

**Columns**:
1. id (SERIAL PRIMARY KEY) - Auto-incrementing unique identifier
2. user_id (VARCHAR NOT NULL INDEX) - Links to user who owns the task
3. title (VARCHAR NOT NULL) - Task title
4. description (TEXT) - Optional detailed description
5. completed (BOOLEAN DEFAULT FALSE) - Completion status
6. created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP) - Creation timestamp
7. updated_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP) - Last update timestamp

### Indexes:
- Primary Key index on id
- Index on user_id for efficient user-based queries

## 3. SQLModel Representation

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
import os

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

## 4. User Isolation Implementation

The data model enforces user isolation by:
- Including a user_id field in each task record
- Requiring all database queries to filter by the authenticated user's ID
- Preventing cross-user data access at the database level
- Supporting the JWT-based authentication requirements