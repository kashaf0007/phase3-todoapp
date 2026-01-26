from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
import os
from typing import List, Optional

from backend.database.connection import engine
from backend.database.init_db import create_db_and_tables
from backend.database.deps import get_session
from backend.src.models.task import Task  # Updated import path to use src models
from backend.app.services.task_service import TaskService  # Updated import path


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

# Configure CORS to allow frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "https://todo-app-frontend.vercel.app"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Additional origins can be added as needed
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API with Neon PostgreSQL"}


@app.post("/tasks/", response_model=Task)
def create_task(
    user_id: str = Body(..., embed=True),
    title: str = Body(..., embed=True),
    description: Optional[str] = Body(None, embed=True),
    session: Session = Depends(get_session)
):
    """
    Create a new task.
    """
    try:
        task = TaskService.create_task(
            session=session,
            user_id=user_id,
            title=title,
            description=description
        )
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/{user_id}", response_model=List[Task])
def get_tasks_for_user(
    user_id: str,
    session: Session = Depends(get_session)
):
    """
    Get all tasks for a specific user.
    """
    try:
        tasks = TaskService.get_tasks_for_user(
            session=session,
            user_id=user_id
        )
        return tasks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    user_id: str = Body(..., embed=True),
    title: Optional[str] = Body(None, embed=True),
    description: Optional[str] = Body(None, embed=True),
    completed: Optional[bool] = Body(None, embed=True),
    session: Session = Depends(get_session)
):
    """
    Update an existing task.
    """
    try:
        task = TaskService.update_task(
            session=session,
            task_id=task_id,
            user_id=user_id,
            title=title,
            description=description,
            completed=completed
        )
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    user_id: str,
    session: Session = Depends(get_session)
):
    """
    Delete a task.
    """
    try:
        success = TaskService.delete_task(
            session=session,
            task_id=task_id,
            user_id=user_id
        )
        if success:
            return {"message": "Task deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.patch("/tasks/{task_id}/complete", response_model=Task)
def toggle_task_completion(
    task_id: int,
    user_id: str,
    session: Session = Depends(get_session)
):
    """
    Toggle task completion status.
    """
    try:
        task = TaskService.toggle_task_completion(
            session=session,
            task_id=task_id,
            user_id=user_id
        )
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))