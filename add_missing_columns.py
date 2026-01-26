"""
Script to add missing columns (tags, category) to the existing tasks table.
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

# SQL commands to add missing columns if they don't exist
sql_commands = [
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS tags TEXT;",
    "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS category VARCHAR(100);"
]

try:
    with engine.connect() as connection:
        for command in sql_commands:
            print(f"Executing: {command}")
            connection.execute(text(command))
            connection.commit()
            print("Command executed successfully.")
    
    print("\nColumns added successfully to the tasks table!")
    
except Exception as e:
    print(f"Error occurred: {e}")
    print("This might happen if you're using an older version of PostgreSQL that doesn't support 'IF NOT EXISTS' in ALTER TABLE.")
    print("In that case, you'll need to manually add the columns or upgrade PostgreSQL.")