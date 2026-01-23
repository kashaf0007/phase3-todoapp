# Quickstart Guide: Neon PostgreSQL Setup & Table Visibility

## Overview
This guide provides step-by-step instructions to set up Neon PostgreSQL for the Todo application, ensuring data persistence and visibility in the Neon dashboard.

## Prerequisites
- Neon.tech account
- Python 3.9+ with pip
- Docker (optional, for containerized setup)
- Git for version control

## Step 1: Set Up Neon PostgreSQL

1. **Create a Neon Account**:
   - Go to [Neon.tech](https://neon.tech)
   - Sign up for a free account

2. **Create a New Project**:
   - Log in to your Neon console
   - Click "New Project"
   - Choose a project name (e.g., "todo-phase2")
   - Select your preferred region
   - Click "Create Project"

3. **Get Connection Details**:
   - Once the project is created, navigate to the "Connection Details" section
   - Note the connection string in the format:
     ```
     postgresql://username:password@ep-xxxxxxx.us-east-1.aws.neon.tech:5432/neondb
     ```

## Step 2: Configure Environment Variables

1. **Create .env file** in the backend directory:
   ```bash
   cd backend
   touch .env
   ```

2. **Add the connection string** to your `.env` file:
   ```
   DATABASE_URL=postgresql://neondb_owner:your_password_here@ep-xxxxxxx.us-east-1.aws.neon.tech:5432/neondb
   ```

3. **Ensure .env is in .gitignore**:
   - Verify that `.env` is listed in your `.gitignore` file to prevent committing credentials

## Step 3: Install Required Dependencies

1. **Install SQLModel and related packages**:
   ```bash
   pip install sqlmodel sqlalchemy psycopg2-binary
   ```

2. **Update pyproject.toml** to include these dependencies if using Poetry:
   ```toml
   [tool.poetry.dependencies]
   sqlmodel = "^0.0.8"
   psycopg2-binary = "^2.9.5"
   ```

## Step 4: Implement SQLModel Models

1. **Create a models.py file** in your backend:
   ```python
   from sqlmodel import SQLModel, Field
   from datetime import datetime
   from typing import Optional

   class Task(SQLModel, table=True):
       id: Optional[int] = Field(default=None, primary_key=True)
       user_id: str = Field(index=True)
       title: str
       description: Optional[str] = None
       completed: bool = False
       created_at: datetime = Field(default_factory=datetime.utcnow)
       updated_at: datetime = Field(default_factory=datetime.utcnow)
   ```

2. **Create database connection utilities**:
   ```python
   from sqlmodel import create_engine
   import os
   from dotenv import load_dotenv

   # Load environment variables
   load_dotenv()

   DATABASE_URL = os.getenv("DATABASE_URL")
   engine = create_engine(DATABASE_URL)

   def create_db_and_tables():
       SQLModel.metadata.create_all(engine)
   ```

## Step 5: Initialize Database Tables

1. **Update your FastAPI application** to initialize the database:
   ```python
   from fastapi import FastAPI
   from contextlib import asynccontextmanager
   from .models import create_db_and_tables

   @asynccontextmanager
   async def lifespan(app: FastAPI):
       # Initialize database tables
       create_db_and_tables()
       yield

   app = FastAPI(lifespan=lifespan)
   ```

2. **Run the application** to create tables:
   ```bash
   uvicorn main:app --reload
   ```

## Step 6: Verify in Neon Dashboard

1. **Go to your Neon Dashboard**:
   - Visit https://console.neon.tech
   - Navigate to your project

2. **Check the Tables section**:
   - You should see the `tasks` table listed
   - Verify that the schema matches the specification:
     - id (integer, primary key, auto increment)
     - user_id (string, not null, indexed)
     - title (string, not null)
     - description (text, nullable)
     - completed (boolean, default false)
     - created_at (timestamp, auto-generated)
     - updated_at (timestamp, auto-updated)

## Step 7: Test Backend Connectivity

1. **Perform a test operation**:
   - Make a POST request to create a task
   - Verify the task appears in the Neon dashboard
   - Make a GET request to retrieve tasks
   - Restart your backend and verify data persists

2. **Check logs** for successful database connections

## Troubleshooting

### Common Issues:

1. **Connection refused**:
   - Verify the connection string format
   - Check that SSL is enabled in the connection string
   - Ensure your IP is not blocked by Neon's security settings

2. **Authentication failed**:
   - Double-check the username and password in the connection string
   - Verify that the role has necessary permissions

3. **Tables not appearing**:
   - Ensure the `create_db_and_tables()` function is called
   - Check that the SQLModel models are properly defined with `table=True`
   - Verify that the application has proper permissions to create tables

4. **Environment variables not loaded**:
   - Confirm that python-dotenv is installed and used
   - Verify the .env file is in the correct directory
   - Check that the environment variable name matches exactly

## Next Steps

Once the database is set up and verified:

1. Implement the API endpoints according to the contract
2. Integrate JWT authentication with the database operations
3. Add user isolation logic to ensure users can only access their own tasks
4. Test all CRUD operations with proper authentication
5. Verify data persistence across application restarts