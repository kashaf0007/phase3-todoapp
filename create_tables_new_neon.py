import os
from sqlmodel import SQLModel, create_engine

# Set the DATABASE_URL environment variable with your new URL
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_TktC9FJmPig5@ep-autumn-recipe-ade5hdh4-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Import the Task model
from backend.models.task import Task

# Get the database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debugging

def create_db_and_tables():
    """
    Creates all database tables based on SQLModel definitions.
    This function should be called when the application starts.
    """
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    print("Creating database tables in your Neon database...")
    create_db_and_tables()
    print("Tables should now be visible in your Neon dashboard!")