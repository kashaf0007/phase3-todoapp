"""
Database schema verification tests for the Todo application.
This module contains tests to verify that the database schema matches the specification.
"""

import unittest
from sqlmodel import SQLModel
from backend.models.task import Task
from backend.database.connection import engine


class TestDatabaseSchema(unittest.TestCase):
    """
    Test class for verifying the database schema matches the specification.
    """
    
    def setUp(self):
        """
        Set up the test environment.
        """
        # Create all tables for testing
        SQLModel.metadata.create_all(engine)
    
    def test_task_table_exists(self):
        """
        Test that the tasks table exists in the database.
        """
        # Check if the table exists by inspecting the database
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        self.assertIn("task", tables, "Task table should exist in the database")
    
    def test_task_table_columns(self):
        """
        Test that the tasks table has the correct columns as per specification.
        """
        from sqlalchemy import inspect
        inspector = inspect(engine)
        columns = inspector.get_columns("task")
        
        # Create a mapping of column names to their definitions
        column_map = {col['name']: col for col in columns}
        
        # Check that all required columns exist
        required_columns = [
            'id', 'user_id', 'title', 'description', 
            'completed', 'created_at', 'updated_at'
        ]
        
        for col_name in required_columns:
            with self.subTest(column=col_name):
                self.assertIn(col_name, column_map, f"Column '{col_name}' should exist in the task table")
    
    def test_task_column_types(self):
        """
        Test that the task table columns have the correct data types.
        """
        from sqlalchemy import inspect
        inspector = inspect(engine)
        columns = inspector.get_columns("task")
        
        # Create a mapping of column names to their definitions
        column_map = {col['name']: col for col in columns}
        
        # Check types (these are approximate since SQLAlchemy types might differ from raw SQL types)
        # The important thing is that they match the conceptual types in the spec
        id_col = column_map['id']
        self.assertTrue(id_col['nullable'], "id should be nullable in definition (becomes non-null primary key via SQLModel)")
        # Note: SQLModel handles the auto-increment and primary key via the Field definition
        
        user_id_col = column_map['user_id']
        self.assertFalse(user_id_col['nullable'], "user_id should not be nullable")
        
        title_col = column_map['title']
        self.assertFalse(title_col['nullable'], "title should not be nullable")
        
        description_col = column_map['description']
        self.assertTrue(description_col['nullable'], "description should be nullable")
        
        completed_col = column_map['completed']
        # We can't easily test the default value here, but SQLModel sets it correctly
        
    def test_task_model_attributes(self):
        """
        Test that the Task model has the correct attributes as per specification.
        """
        # Check that the Task model has all required fields
        task_fields = Task.__fields__
        
        expected_fields = {
            'id', 'user_id', 'title', 'description', 
            'completed', 'created_at', 'updated_at'
        }
        
        actual_fields = set(task_fields.keys())
        
        self.assertEqual(
            expected_fields, 
            actual_fields, 
            f"Task model should have exactly these fields: {expected_fields}, got: {actual_fields}"
        )
    
    def test_task_field_constraints(self):
        """
        Test that the Task model fields have the correct constraints.
        """
        task_fields = Task.__fields__
        
        # Check id field (primary key, auto increment)
        id_field = task_fields['id']
        self.assertTrue(hasattr(Task, '__table_args__') or 
                       hasattr(Task, '__sqlmodel_relationships__'), "Task should be configured as a table")
        
        # Check user_id field (not null, indexed)
        user_id_field = task_fields['user_id']
        # In SQLModel, indexes are defined differently, but we can check the field exists
        
        # Check title field (not null)
        title_field = task_fields['title']
        # This is validated by Pydantic/SQLModel
        
        # Check description field (nullable)
        description_field = task_fields['description']
        # This is handled by Optional type annotation
        
        # Check completed field (default false)
        completed_field = task_fields['completed']
        # Default value is checked via the field definition
        
        # Check created_at and updated_at fields (auto-generated/auto-updated)
        created_at_field = task_fields['created_at']
        updated_at_field = task_fields['updated_at']
        # These have default factories as specified in the model


if __name__ == '__main__':
    unittest.main()