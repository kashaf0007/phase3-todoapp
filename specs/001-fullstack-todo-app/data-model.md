# Data Model: Phase II Full-Stack Todo Application

**Feature**: 001-fullstack-todo-app
**Date**: 2025-12-30
**Input**: @specs/001-fullstack-todo-app/spec.md (Key Entities, FR-019 through FR-026)

## Overview

This document defines the database schema for Phase II multi-user todo application. The data model enforces strict user isolation with every task belonging to exactly one user. All entities use SQLModel for type-safe database operations with Neon Serverless PostgreSQL.

## Entities

### User

Represents an authenticated account holder who owns tasks. User management handled by Better Auth on the frontend; backend references users via user_id in task ownership.

**Table Name**: `users`

**Fields**:

| Field         | Type     | Constraints                  | Description                                    |
|---------------|----------|------------------------------|------------------------------------------------|
| id            | string   | PRIMARY KEY, UUID            | Unique user identifier (UUID v4 format)        |
| email         | string   | UNIQUE, NOT NULL, indexed    | User's email address for authentication        |
| password_hash | string   | NOT NULL                     | Bcrypt hashed password (managed by Better Auth)|
| created_at    | datetime | NOT NULL, default=now()      | Account creation timestamp                     |

**Indexes**:
- Primary key index on `id` (automatic)
- Unique index on `email` for authentication lookup (FR-003)

**Relationships**:
- One-to-many with Task: `User.tasks → Task[]`

**Validation Rules**:
- Email format: Must match RFC 5322 email regex (enforced by Better Auth)
- Email uniqueness: Case-insensitive (user@example.com == USER@example.com) per Assumption 8
- Password: Minimum 8 characters (enforced by Better Auth, Assumption 1)

**Security Notes**:
- Password stored as bcrypt hash only (never plaintext per FR-007)
- password_hash field NEVER exposed in API responses
- User records managed by Better Auth; backend only reads for task ownership validation

**Lifecycle**:
- Created: Better Auth handles registration flow
- Updated: Password changes handled by Better Auth (out of scope for Phase II per forbidden features)
- Deleted: User deletion out of scope for Phase II

---

### Task

Represents a single todo item belonging to exactly one user. Tasks are the core entity of the application, supporting five basic operations (create, view, update, delete, mark complete).

**Table Name**: `tasks`

**Fields**:

| Field       | Type     | Constraints                          | Description                                    |
|-------------|----------|--------------------------------------|------------------------------------------------|
| id          | integer  | PRIMARY KEY, AUTO_INCREMENT          | Unique task identifier                         |
| user_id     | string   | FOREIGN KEY (users.id), NOT NULL, indexed | Owner of this task (UUID reference)      |
| title       | string   | NOT NULL, max_length=255             | Task title (required)                          |
| description | text     | NULL, max_length=2000                | Optional task description                      |
| completed   | boolean  | NOT NULL, default=False              | Completion status (False = incomplete)         |
| created_at  | datetime | NOT NULL, default=now()              | Task creation timestamp                        |
| updated_at  | datetime | NOT NULL, default=now(), auto_update | Last modification timestamp                    |

**Indexes**:
- Primary key index on `id` (automatic)
- Index on `user_id` for efficient user-scoped queries (FR-020, Assumption 5)
- Composite index on `(user_id, created_at)` for default sort order (newest first)

**Relationships**:
- Many-to-one with User: `Task.user → User` via `user_id` foreign key

**Validation Rules**:
- **title**:
  - Required (non-empty string per FR-024)
  - Maximum 255 characters (Assumption 7)
  - Whitespace-only titles rejected (trimmed length > 0)
- **description**:
  - Optional (can be null or empty per FR-025)
  - Maximum 2000 characters (Assumption 7)
- **user_id**:
  - Required (NOT NULL per FR-020)
  - Must reference existing user in `users` table (foreign key constraint)
- **completed**:
  - Defaults to False on creation (FR-026)
  - Only accepts True/False values (boolean type)
- **updated_at**:
  - Auto-updated on any field modification (FR-023)
  - Implemented via SQLModel's `onupdate` trigger

**Foreign Key Constraints**:
- `user_id` → `users.id`: ON DELETE CASCADE (deleting user removes their tasks)
- Foreign key enforced at database level for data integrity

**Security Enforcement**:
- All queries MUST filter by `user_id = current_user.id` (FR-048)
- Backend MUST verify task ownership before update/delete operations (FR-049)
- User cannot access tasks where `user_id != current_user.id` (403 Forbidden per FR-036)

**Default Ordering**:
- Tasks ordered by `created_at DESC` (newest first) per Assumption 5
- No sorting, filtering, or search capabilities in Phase II (forbidden features)

**Lifecycle**:
- Created: User submits title + optional description via POST endpoint
- Updated: User modifies title/description via PUT endpoint, or toggles completion via PATCH endpoint
- Deleted: User permanently removes task via DELETE endpoint (no soft delete in Phase II)

---

## Entity Relationships

```
User (1) ----< (N) Task
  |                  |
  | id (PK)          | id (PK)
  |                  | user_id (FK → User.id)
  | email (unique)   | title
  | password_hash    | description
  | created_at       | completed
                     | created_at
                     | updated_at
```

**Relationship Type**: One-to-Many
- One User can have zero or more Tasks
- Each Task belongs to exactly one User

**Referential Integrity**:
- Foreign key constraint ensures task.user_id always references valid user
- Cascade delete: Deleting user removes all their tasks (not implemented in Phase II UI)

**Isolation Guarantee**:
- All task queries filtered by user_id
- No cross-user task visibility possible at database or application level

---

## SQLModel Schema Specifications

### User Model

```
Table: users
Managed by: Better Auth (frontend)
Backend usage: Read-only for task ownership validation

Fields:
  id: str (UUID) - Primary key
  email: str - Unique, indexed
  password_hash: str - Bcrypt hash
  created_at: datetime - Auto-set on creation

Relationships:
  tasks: List[Task] - One-to-many relationship
```

### Task Model

```
Table: tasks
Managed by: Backend FastAPI application
CRUD operations: Full control (create, read, update, delete)

Fields:
  id: int - Primary key, auto-increment
  user_id: str - Foreign key to users.id, NOT NULL, indexed
  title: str - Max 255 chars, NOT NULL
  description: Optional[str] - Max 2000 chars, nullable
  completed: bool - Default False, NOT NULL
  created_at: datetime - Auto-set on creation
  updated_at: datetime - Auto-updated on modification

Relationships:
  user: User - Many-to-one relationship via user_id
```

---

## Database Initialization

### Table Creation

Tables created via SQLModel's `SQLModel.metadata.create_all(engine)` method during application startup. No migrations framework (Alembic) in Phase II; schema changes require manual table recreation in development.

### Initial Data

No seed data required. Users created via Better Auth registration flow. Tasks created by users via application interface.

### Connection Configuration

- Database: Neon Serverless PostgreSQL
- Connection: Via DATABASE_URL environment variable
- Format: `postgresql://user:password@host/database?sslmode=require`
- Connection pooling: SQLAlchemy engine default (5 connections, 10 max overflow)

---

## Data Constraints Summary

**User Constraints**:
- Email uniqueness (case-insensitive)
- Password minimum 8 characters (Better Auth enforced)
- Email format validation (RFC 5322)

**Task Constraints**:
- Title required (1-255 characters)
- Description optional (0-2000 characters)
- User_id must reference existing user (foreign key)
- Completed defaults to False
- Updated_at auto-updates on modification

**Security Constraints**:
- All task operations filtered by authenticated user_id
- No cross-user data access permitted
- JWT-derived user_id used exclusively (never from client input)

---

## Performance Considerations

### Index Strategy

1. **user_id index on tasks**: Essential for user-scoped queries (`WHERE user_id = ?`)
   - Expected query pattern: Fetch all tasks for authenticated user
   - Index selectivity: High (distributes evenly across users)
   - Query performance: O(log N) instead of O(N) full table scan

2. **email unique index on users**: Required for authentication lookup
   - Expected query pattern: Find user by email during login
   - Index selectivity: Perfect (unique constraint)
   - Query performance: O(log N) hash index lookup

3. **Composite index (user_id, created_at) on tasks**: Optimizes default sort order
   - Expected query pattern: Fetch user's tasks ordered by newest first
   - Index covers both filter and sort operations
   - Eliminates separate sort step (index scan returns sorted results)

### Query Optimization

**Common Queries**:
- List user's tasks: `SELECT * FROM tasks WHERE user_id = ? ORDER BY created_at DESC`
  - Uses composite index (user_id, created_at)
  - Expected rows: <100 per user (SC-003 performance target)
  - Query time: <100ms

- Get single task: `SELECT * FROM tasks WHERE id = ? AND user_id = ?`
  - Uses primary key + user_id filter
  - Expected rows: 0 or 1
  - Query time: <10ms

- Create task: `INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at) VALUES (...)`
  - Single row insert
  - Expected time: <50ms

- Update task: `UPDATE tasks SET title = ?, description = ?, updated_at = ? WHERE id = ? AND user_id = ?`
  - Single row update with ownership verification
  - Expected time: <50ms

- Delete task: `DELETE FROM tasks WHERE id = ? AND user_id = ?`
  - Single row delete with ownership verification
  - Expected time: <50ms

**Performance Targets** (from SC-003, SC-002):
- Task list load: <2 seconds for 100 tasks
- Task create/update/delete: <10 seconds total (includes network + DB)
- Expected database query time: <500ms for list, <100ms for single operations

---

## Scalability Notes

**Phase II Scale** (per SC-010):
- Target: 10+ concurrent users minimum
- Expected load: Low (development/testing phase)
- Connection pool (5 + 10 overflow) sufficient for this scale

**Future Scaling Considerations** (out of scope for Phase II):
- Add caching layer (Redis) for frequently accessed task lists
- Implement pagination for users with >100 tasks
- Consider read replicas for high read:write ratios
- Add database-level row-level security (RLS) as defense-in-depth
- Implement soft delete (deleted_at timestamp) instead of hard delete

---

## Data Model Validation Checklist

- [x] All entities defined with complete field specifications
- [x] Primary keys specified for both entities
- [x] Foreign key relationship (task.user_id → user.id) defined
- [x] Indexes identified for performance optimization
- [x] Validation rules documented for all fields
- [x] Security constraints specified (user isolation enforcement)
- [x] Default values documented (completed=False, timestamps)
- [x] Field lengths constrained (title 255, description 2000)
- [x] Referential integrity enforced (foreign key constraints)
- [x] Relationship cardinality documented (one-to-many)
- [x] No forbidden features included (no priorities, tags, dates, etc.)
- [x] All requirements from spec (FR-019 through FR-026) satisfied

**Status**: ✅ **COMPLETE** - Data model ready for implementation

**Next Artifact**: contracts/api-spec.yaml (OpenAPI 3.0 REST API specification)
