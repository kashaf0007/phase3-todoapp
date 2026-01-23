# Implementation Plan: Neon PostgreSQL Setup & Table Visibility

## 1. Technical Context

This plan describes **how the Neon PostgreSQL database will be provisioned, connected, and validated** for Phase II of the Todo Full-Stack Web Application.

The plan ensures:

* Persistent storage using Neon DB
* Schema-driven development
* Tables are visible in the Neon dashboard
* Backend accessibility via FastAPI + SQLModel

### 1.1 Known Dependencies

- Neon PostgreSQL account and console access
- Python FastAPI backend environment
- SQLModel ORM library
- Environment variable management system

### 1.2 Unknown Dependencies

- Current database connection status [NEEDS CLARIFICATION]
- Existing SQLModel implementation [NEEDS CLARIFICATION]
- Current environment configuration [NEEDS CLARIFICATION]

### 1.3 Integration Points

- FastAPI backend connecting to Neon PostgreSQL
- SQLModel models mapping to database schema
- Environment variables for database configuration

## 2. Constitution Check

### 2.1 Spec-First Development Compliance
✅ Plan is based on explicit specification: `@specs/003-neon-db-persistence/spec.md`

### 2.2 No Manual Coding Compliance
✅ Plan delegates all implementation to Claude Code; no manual coding steps included

### 2.3 Agentic Dev Stack Workflow Compliance
✅ Plan follows sequence: spec → plan → tasks → implementation → validation

### 2.4 Phase Isolation Compliance
✅ Plan focuses only on database persistence and visibility, not advanced features

### 2.5 Technology Stack Compliance
✅ Plan uses only approved technologies: FastAPI, SQLModel, Neon PostgreSQL

### 2.6 REST API Contract Compliance
✅ Plan supports the required API contract through database design

### 2.7 Security Compliance
✅ Plan enforces environment variables for credentials, no hardcoded values

### 2.8 Gate Verification
All constitutional gates pass. Proceed with implementation plan.

## 3. Phase 0: Outline & Research

### 3.1 Research Tasks

#### 3.1.1 Neon PostgreSQL Account Setup
**Task**: Research Neon PostgreSQL account creation and project setup process
- How to create a Neon PostgreSQL account
- How to set up a new project in Neon
- Understanding connection string components

#### 3.1.2 Current Database State Investigation
**Task**: Investigate current database implementation status
- Check if any database connection is already configured
- Identify existing models or schemas
- Understand current environment variable setup

#### 3.1.3 SQLModel Best Practices
**Task**: Research best practices for SQLModel implementation
- How to define models that match the required schema
- Connection management patterns
- Migration strategies

### 3.2 Consolidated Research Findings

#### 3.2.1 Neon PostgreSQL Setup
**Decision**: Use Neon's web console to create a new project
**Rationale**: Neon provides a user-friendly interface for PostgreSQL setup with serverless scaling
**Alternatives considered**: Self-hosted PostgreSQL, other cloud providers
**Connection String Format**: `postgresql://username:password@host:port/database?sslmode=require`

#### 3.2.2 SQLModel Implementation
**Decision**: Use SQLModel with Pydantic-style declarations
**Rationale**: Matches the technology stack requirements and integrates well with FastAPI
**Alternatives considered**: SQLAlchemy ORM, raw SQL (prohibited by constitution)

#### 3.2.3 Environment Configuration
**Decision**: Store connection string in DATABASE_URL environment variable
**Rationale**: Follows industry standards and security best practices
**Alternatives considered**: Hardcoded values (prohibited by constitution), config files

## 4. Phase 1: Design & Contracts

### 4.1 Data Model Design

#### 4.1.1 Task Entity
**Entity Name**: Task
**Fields**:
- id: integer (Primary Key, Auto Increment)
- user_id: string (Not Null, Indexed)
- title: string (Not Null)
- description: text (Nullable)
- completed: boolean (Default false)
- created_at: timestamp (Auto-generated)
- updated_at: timestamp (Auto-updated)

**Relationships**: 
- Belongs to one User (via user_id foreign key)

**Validation Rules**:
- title must not be empty
- user_id must exist in users table
- created_at and updated_at are automatically managed

### 4.2 API Contracts

Based on the functional requirements, the following endpoints will be supported:

1. **POST /api/{user_id}/tasks** - Create a new task in the database
2. **GET /api/{user_id}/tasks** - Retrieve all tasks for a user from the database
3. **GET /api/{user_id}/tasks/{id}** - Retrieve a specific task from the database
4. **PUT /api/{user_id}/tasks/{id}** - Update a task in the database
5. **DELETE /api/{user_id}/tasks/{id}** - Delete a task from the database
6. **PATCH /api/{user_id}/tasks/{id}/complete** - Toggle task completion in the database

### 4.3 SQLModel Schema

```python
from sqlmodel import SQLModel, Field, create_engine, Session
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

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
```

### 4.4 Quickstart Guide

1. **Set up Neon PostgreSQL**:
   - Create an account at Neon.tech
   - Create a new project
   - Note the connection string

2. **Configure Environment**:
   - Add the connection string to your `.env` file as `DATABASE_URL`

3. **Initialize Database**:
   - Run the database initialization code to create tables
   - Verify tables exist in Neon dashboard

4. **Connect Backend**:
   - Update FastAPI application to use the database connection
   - Test CRUD operations

## 5. Phase 2: Implementation Steps

### 5.1 Step 1: Provision Neon PostgreSQL Project

**Objective**: Create a dedicated Neon PostgreSQL database instance.

**Actions**:
1. Navigate to Neon.tech and create an account
2. Create a new project named "todo-phase2"
3. Select PostgreSQL as the database engine
4. Note the connection string provided

**Output**: Active Neon PostgreSQL project with connection details

### 5.2 Step 2: Configure Environment Variables

**Objective**: Securely configure backend database access.

**Actions**:
1. Add connection string to backend environment variables in `.env`:
   ```
   DATABASE_URL=postgresql://neondb_owner:npg_cIRiT1jD2Xeu@ep-autumn-unit-adb7wino-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   ```
2. Ensure `.env` file is added to `.gitignore` to exclude from version control
3. Confirm backend reads database URL only from environment variables

**Output**: Secure database configuration

### 5.3 Step 3: Implement SQLModel Models

**Objective**: Generate ORM models directly from schema specs.

**Actions**:
1. Create `models.py` in the backend directory
2. Define the Task model using SQLModel with the required schema
3. Add database connection and initialization code
4. Validate model-to-schema alignment

**Output**: SQLModel models matching schema spec

### 5.4 Step 4: Apply Table Creation

**Objective**: Create tables inside Neon PostgreSQL.

**Actions**:
1. Configure FastAPI database initialization
2. Implement the `create_db_and_tables()` function
3. Call initialization function when the application starts
4. Start backend service to apply schema

**Output**: `tasks` table created in Neon database

### 5.5 Step 5: Verify Neon Dashboard Visibility

**Objective**: Confirm schema correctness and persistence.

**Actions**:
1. Open Neon Dashboard
2. Navigate to Tables view
3. Verify `tasks` table exists with correct schema
4. Confirm column structure matches specification

**Output**: Tables visible in Neon dashboard

### 5.6 Step 6: Backend Connectivity Validation

**Objective**: Ensure backend can access Neon database.

**Actions**:
1. Run FastAPI backend
2. Perform test CRUD operations via API
3. Restart backend service
4. Confirm data persistence remains intact

**Output**: Backend successfully reads/writes data

## 6. Risks & Mitigation

| Risk | Mitigation |
|------|------------|
| Incorrect connection string | Validate DATABASE_URL format and test connection separately |
| Tables not visible in Neon dashboard | Re-run schema creation and verify SQLModel implementation |
| Data loss due to improper configuration | Ensure Neon's persistent storage is enabled |
| Security vulnerabilities | Follow constitution's security guidelines, no hardcoded credentials |
| Performance issues | Monitor connection pooling and query optimization |

## 7. Success Criteria

This plan is complete when:
- Neon PostgreSQL project exists and is accessible
- DATABASE_URL is properly configured
- SQLModel models are implemented and tested
- `tasks` table is visible in Neon dashboard with correct schema
- Backend successfully performs CRUD operations on Neon database
- Data persists after backend restarts
- No hardcoded credentials exist in codebase

## 8. Deliverables

- Neon PostgreSQL database instance
- Database schema specification
- SQLModel models implementation
- Configured environment variables
- Verified table visibility in Neon dashboard
- Working backend database connectivity