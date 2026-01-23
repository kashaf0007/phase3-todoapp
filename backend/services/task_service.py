"""
Task CRUD service for the Todo application.
This module provides all the business logic for managing tasks.
"""

from typing import List, Optional
from sqlmodel import Session, select
from ..models.task import Task
from ..database.errors import TaskNotFoundError


class TaskService:
    """
    Service class for handling all task-related operations.
    """
    
    @staticmethod
    def create_task(session: Session, user_id: str, title: str, description: Optional[str] = None) -> Task:
        """
        Creates a new task for a user.
        
        Args:
            session: Database session
            user_id: ID of the user creating the task
            title: Title of the task
            description: Optional description of the task
            
        Returns:
            The created Task object
        """
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    
    @staticmethod
    def get_tasks_for_user(session: Session, user_id: str) -> List[Task]:
        """
        Retrieves all tasks for a specific user.
        
        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            
        Returns:
            List of Task objects belonging to the user
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return tasks
    
    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: str) -> Task:
        """
        Retrieves a specific task by its ID for a user.
        
        Args:
            session: Database session
            task_id: ID of the task to retrieve
            user_id: ID of the user requesting the task
            
        Returns:
            The Task object if found
            
        Raises:
            TaskNotFoundError: If the task doesn't exist or doesn't belong to the user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found for user {user_id}")
        return task
    
    @staticmethod
    def update_task(session: Session, task_id: int, user_id: str, 
                    title: Optional[str] = None, description: Optional[str] = None, 
                    completed: Optional[bool] = None) -> Task:
        """
        Updates an existing task for a user.
        
        Args:
            session: Database session
            task_id: ID of the task to update
            user_id: ID of the user requesting the update
            title: New title for the task (optional)
            description: New description for the task (optional)
            completed: New completion status for the task (optional)
            
        Returns:
            The updated Task object
            
        Raises:
            TaskNotFoundError: If the task doesn't exist or doesn't belong to the user
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        
        # Update only the fields that were provided
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        
        task.updated_at = task.__class__.updated_at.default.arg  # Update timestamp
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    
    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> bool:
        """
        Deletes a specific task for a user.
        
        Args:
            session: Database session
            task_id: ID of the task to delete
            user_id: ID of the user requesting the deletion
            
        Returns:
            True if the task was deleted, False otherwise
            
        Raises:
            TaskNotFoundError: If the task doesn't exist or doesn't belong to the user
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        session.delete(task)
        session.commit()
        return True
    
    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: str) -> Task:
        """
        Toggles the completion status of a specific task for a user.
        
        Args:
            session: Database session
            task_id: ID of the task to toggle
            user_id: ID of the user requesting the toggle
            
        Returns:
            The updated Task object with toggled completion status
            
        Raises:
            TaskNotFoundError: If the task doesn't exist or doesn't belong to the user
        """
        task = TaskService.get_task_by_id(session, task_id, user_id)
        task.completed = not task.completed
        task.updated_at = task.__class__.updated_at.default.arg  # Update timestamp
        
        session.add(task)
        session.commit()
        session.refresh(task)
        return task