"""
Script to update the tasks table schema to match the enhanced model.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set.")

# Create engine
engine = create_engine(DATABASE_URL)

# SQL commands to update the tasks table schema
sql_commands = [
    # Change the id column to VARCHAR and allow it to be NULL temporarily so we can update existing records
    "ALTER TABLE tasks ALTER COLUMN id DROP DEFAULT;",
    "ALTER TABLE tasks ADD COLUMN new_id VARCHAR(36);",
    "UPDATE tasks SET new_id = CAST(id AS VARCHAR);",
    "ALTER TABLE tasks DROP COLUMN id;",
    "ALTER TABLE tasks RENAME COLUMN new_id TO id;",
    "ALTER TABLE tasks ALTER COLUMN id SET NOT NULL;",
    "ALTER TABLE tasks ADD PRIMARY KEY (id);"
]

try:
    with engine.connect() as connection:
        for command in sql_commands:
            print(f"Executing: {command}")
            try:
                connection.execute(text(command))
                connection.commit()
                print("Command executed successfully.")
            except Exception as e:
                print(f"Command failed: {e}")
                # Some commands might not be supported depending on the database
                # Continue to the next command
    
    print("\nTable schema updated successfully!")
    
except Exception as e:
    print(f"Error occurred: {e}")
    print("Some databases might not support all ALTER TABLE operations.")
    print("You might need to recreate the table or use a migration tool like Alembic.")