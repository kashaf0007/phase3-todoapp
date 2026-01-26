"""
Script to check the current tasks table schema.
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

# SQL command to check the table structure
sql_commands = [
    "SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name = 'tasks' ORDER BY ordinal_position;"
]

try:
    with engine.connect() as connection:
        for command in sql_commands:
            print(f"Executing: {command}")
            result = connection.execute(text(command))
            rows = result.fetchall()
            
            print("Current tasks table schema:")
            for row in rows:
                print(f"  {row[0]}: {row[1]}, nullable: {row[2]}")
    
except Exception as e:
    print(f"Error occurred: {e}")