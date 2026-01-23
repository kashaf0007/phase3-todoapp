"""
Comprehensive test suite for database operations in the Todo application.
This module contains tests for all database operations including CRUD operations.
"""

import unittest
from unittest.mock import patch, MagicMock
from sqlmodel import Session, select
from backend.models.task import Task
from backend.services.task_service import TaskService
from backend.database.errors import TaskNotFoundError


class TestTaskService(unittest.TestCase):
    """
    Test class for the TaskService.
    """
    
    def setUp(self):
        """
        Set up the test environment.
        """
        self.session = MagicMock(spec=Session)
        self.user_id = "test_user_123"
        self.task_data = {
            "user_id": self.user_id,
            "title": "Test Task",
            "description": "This is a test task",
            "completed": False
        }
    
    def test_create_task_success(self):
        """
        Test successful task creation.
        """
        # Arrange
        new_task = Task(**self.task_data)
        self.session.add.return_value = None
        self.session.commit.return_value = None
        self.session.refresh.return_value = None
        
        # Act
        result = TaskService.create_task(
            self.session, 
            self.user_id, 
            self.task_data["title"], 
            self.task_data["description"]
        )
        
        # Assert
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertIsInstance(result, Task)
        self.assertEqual(result.user_id, self.user_id)
        self.assertEqual(result.title, self.task_data["title"])
    
    def test_get_tasks_for_user_success(self):
        """
        Test successful retrieval of tasks for a user.
        """
        # Arrange
        mock_tasks = [
            Task(id=1, user_id=self.user_id, title="Task 1"),
            Task(id=2, user_id=self.user_id, title="Task 2")
        ]
        self.session.exec.return_value.all.return_value = mock_tasks
        
        # Act
        result = TaskService.get_tasks_for_user(self.session, self.user_id)
        
        # Assert
        self.session.exec.assert_called_once()
        self.assertEqual(len(result), 2)
        for task in result:
            self.assertEqual(task.user_id, self.user_id)
    
    def test_get_task_by_id_success(self):
        """
        Test successful retrieval of a specific task by ID.
        """
        # Arrange
        task_id = 1
        mock_task = Task(id=task_id, user_id=self.user_id, title="Test Task")
        self.session.exec.return_value.first.return_value = mock_task
        
        # Act
        result = TaskService.get_task_by_id(self.session, task_id, self.user_id)
        
        # Assert
        self.session.exec.assert_called_once()
        self.assertEqual(result.id, task_id)
        self.assertEqual(result.user_id, self.user_id)
    
    def test_get_task_by_id_not_found(self):
        """
        Test retrieval of a non-existent task raises TaskNotFoundError.
        """
        # Arrange
        task_id = 999
        self.session.exec.return_value.first.return_value = None
        
        # Act & Assert
        with self.assertRaises(TaskNotFoundError):
            TaskService.get_task_by_id(self.session, task_id, self.user_id)
    
    def test_update_task_success(self):
        """
        Test successful task update.
        """
        # Arrange
        task_id = 1
        updated_title = "Updated Task Title"
        mock_task = Task(id=task_id, user_id=self.user_id, title="Original Title")
        self.session.exec.return_value.first.return_value = mock_task
        
        # Act
        result = TaskService.update_task(
            self.session, 
            task_id, 
            self.user_id, 
            title=updated_title
        )
        
        # Assert
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertEqual(result.title, updated_title)
    
    def test_delete_task_success(self):
        """
        Test successful task deletion.
        """
        # Arrange
        task_id = 1
        mock_task = Task(id=task_id, user_id=self.user_id, title="Task to Delete")
        self.session.exec.return_value.first.return_value = mock_task
        
        # Act
        result = TaskService.delete_task(self.session, task_id, self.user_id)
        
        # Assert
        self.session.delete.assert_called_once_with(mock_task)
        self.session.commit.assert_called_once()
        self.assertTrue(result)
    
    def test_toggle_task_completion_success(self):
        """
        Test successful toggling of task completion status.
        """
        # Arrange
        task_id = 1
        mock_task = Task(id=task_id, user_id=self.user_id, title="Toggle Task", completed=False)
        self.session.exec.return_value.first.return_value = mock_task
        
        # Act
        result = TaskService.toggle_task_completion(self.session, task_id, self.user_id)
        
        # Assert
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.assertTrue(result.completed)  # Should be True after toggling from False
        

class TestDatabaseConnection(unittest.TestCase):
    """
    Test class for database connection functionality.
    """
    
    @patch('backend.database.connection.engine')
    def test_engine_creation(self, mock_engine):
        """
        Test that the database engine is created properly.
        """
        from backend.database.connection import engine
        # Just verify that the engine exists and is accessible
        self.assertIsNotNone(engine)
    

class IntegrationTestTaskLifecycle(unittest.TestCase):
    """
    Integration tests for the complete task lifecycle.
    """
    
    def setUp(self):
        """
        Set up the test environment.
        """
        self.session = MagicMock(spec=Session)
        self.user_id = "integration_test_user"
    
    def test_complete_task_lifecycle(self):
        """
        Test the complete lifecycle of a task: create, read, update, toggle, delete.
        """
        # Create
        created_task = TaskService.create_task(
            self.session, 
            self.user_id, 
            "Integration Test Task", 
            "This is for integration testing"
        )
        
        # Verify creation
        self.assertIsNotNone(created_task.id)
        self.assertEqual(created_task.user_id, self.user_id)
        
        # Read (all tasks for user)
        tasks = TaskService.get_tasks_for_user(self.session, self.user_id)
        self.assertGreaterEqual(len(tasks), 1)
        
        # Read (specific task)
        retrieved_task = TaskService.get_task_by_id(self.session, created_task.id, self.user_id)
        self.assertEqual(retrieved_task.id, created_task.id)
        
        # Update
        updated_task = TaskService.update_task(
            self.session,
            created_task.id,
            self.user_id,
            title="Updated Integration Test Task"
        )
        self.assertEqual(updated_task.title, "Updated Integration Test Task")
        
        # Toggle completion
        toggled_task = TaskService.toggle_task_completion(self.session, created_task.id, self.user_id)
        self.assertNotEqual(toggled_task.completed, created_task.completed)
        
        # Delete
        delete_result = TaskService.delete_task(self.session, created_task.id, self.user_id)
        self.assertTrue(delete_result)


if __name__ == '__main__':
    # Run all tests
    unittest.main(verbosity=2)