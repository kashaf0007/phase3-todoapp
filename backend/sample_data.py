#!/usr/bin/env python3
"""
Sample data insertion script for the Todo application.
This script creates sample tasks to test database visibility in the Neon dashboard.
"""

from datetime import datetime
from sqlmodel import Session
from .database.connection import engine
from .models.task import Task


def insert_sample_data():
    """
    Inserts sample data into the tasks table for testing purposes.
    """
    print("Inserting sample data...")
    
    with Session(engine) as session:
        # Sample tasks for testing
        sample_tasks = [
            Task(
                user_id="user123",
                title="Complete project proposal",
                description="Finish the project proposal document and send for review",
                completed=False
            ),
            Task(
                user_id="user123",
                title="Schedule team meeting",
                description="Arrange a team meeting for next week to discuss progress",
                completed=True
            ),
            Task(
                user_id="user456",
                title="Buy groceries",
                description="Milk, eggs, bread, fruits, and vegetables",
                completed=False
            ),
            Task(
                user_id="user456",
                title="Call plumber",
                description="Fix the leaking faucet in the kitchen",
                completed=False
            )
        ]
        
        for task in sample_tasks:
            session.add(task)
            print(f"Added task: {task.title} for user {task.user_id}")
        
        session.commit()
        print("Sample data inserted successfully!")


if __name__ == "__main__":
    insert_sample_data()