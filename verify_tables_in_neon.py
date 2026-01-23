import os
from sqlmodel import SQLModel, create_engine, Session, select
from backend.models.task import Task

# Set the DATABASE_URL environment variable
os.environ["DATABASE_URL"] = "postgresql://neondb_owner:npg_cIRiT1jD2Xeu@ep-autumn-unit-adb7wino-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

# Get the database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def verify_table_exists():
    """
    Verifies that the task table exists in the database.
    """
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"Tables in database: {tables}")
    
    if "task" in tables:
        print("✅ The 'task' table exists in your Neon database!")
        
        # Get column information
        columns = inspector.get_columns("task")
        print("\nTable structure:")
        for col in columns:
            print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")
        
        return True
    else:
        print("❌ The 'task' table does not exist in your Neon database.")
        return False

def test_crud_operations():
    """
    Tests basic CRUD operations on the task table.
    """
    print("\nTesting CRUD operations...")
    
    with Session(engine) as session:
        # Create a test task
        test_task = Task(
            user_id="test_user",
            title="Test task from verification script",
            description="This is a test to verify the table works",
            completed=False
        )
        
        session.add(test_task)
        session.commit()
        session.refresh(test_task)
        
        print(f"✅ Created task with ID: {test_task.id}")
        
        # Read the task
        statement = select(Task).where(Task.id == test_task.id)
        result = session.exec(statement).first()
        
        if result:
            print(f"✅ Retrieved task: {result.title}")
        
        # Update the task
        result.completed = True
        session.add(result)
        session.commit()
        
        print(f"✅ Updated task completion status to: {result.completed}")
        
        # Delete the task
        session.delete(result)
        session.commit()
        
        print("✅ Deleted the test task")
        
        return True

if __name__ == "__main__":
    print("Verifying table creation in Neon database...\n")
    
    if verify_table_exists():
        print("\nTable verification successful!")
        
        # Run a quick CRUD test
        test_crud_operations()
        
        print("\n🎉 All tests passed! Your Neon database is properly set up with the task table.")
        print("The table should now be visible in your Neon dashboard.")
    else:
        print("\n❌ Table verification failed!")