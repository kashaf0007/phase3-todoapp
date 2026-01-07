"""
Database Connection Diagnostic Script
Tests database connectivity and data persistence to Neon PostgreSQL.
"""

import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlmodel import Session, select, SQLModel
from src.database import engine
from src.models.user import User
from src.models.task import Task


def test_database_connection():
    """Test database connection and schema creation."""
    print("=" * 60)
    print("DATABASE CONNECTION DIAGNOSTIC")
    print("=" * 60)

    # Step 1: Test connection
    print("\n[1] Testing database connection...")
    try:
        with Session(engine) as session:
            result = session.exec(select(1)).first()
            print("✓ Database connection successful!")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False

    # Step 2: Create tables
    print("\n[2] Creating database tables...")
    try:
        SQLModel.metadata.create_all(engine)
        print("✓ Tables created/verified successfully!")
    except Exception as e:
        print(f"✗ Table creation failed: {e}")
        return False

    # Step 3: Check existing data
    print("\n[3] Checking existing data...")
    try:
        with Session(engine) as session:
            user_count = len(session.exec(select(User)).all())
            task_count = len(session.exec(select(Task)).all())
            print(f"   - Users in database: {user_count}")
            print(f"   - Tasks in database: {task_count}")
    except Exception as e:
        print(f"✗ Data query failed: {e}")
        return False

    # Step 4: Test data insertion (create test user and task)
    print("\n[4] Testing data insertion...")
    try:
        with Session(engine) as session:
            # Create or get test user
            test_user_id = "test-diagnostic-user-12345"
            existing_user = session.exec(
                select(User).where(User.id == test_user_id)
            ).first()

            if existing_user:
                print(f"   - Using existing test user: {test_user_id}")
                test_user = existing_user
            else:
                test_user = User(
                    id=test_user_id,
                    email="diagnostic-test@example.com",
                    password_hash="$2b$12$test_hash_for_diagnostic_purposes"
                )
                session.add(test_user)
                session.commit()
                session.refresh(test_user)
                print(f"   - Created new test user: {test_user_id}")

            # Create test task
            test_task = Task(
                user_id=test_user.id,
                title=f"Diagnostic Test Task - {datetime.utcnow().isoformat()}",
                description="This is a test task created by the diagnostic script",
                completed=False
            )
            session.add(test_task)
            session.commit()
            session.refresh(test_task)

            print(f"✓ Test task created successfully! ID: {test_task.id}")
            print(f"   - Title: {test_task.title}")
            print(f"   - Created at: {test_task.created_at}")
    except Exception as e:
        print(f"✗ Data insertion failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Step 5: Verify data persistence (read back)
    print("\n[5] Verifying data persistence...")
    try:
        with Session(engine) as session:
            # Query the test task we just created
            persisted_task = session.exec(
                select(Task).where(Task.id == test_task.id)
            ).first()

            if persisted_task:
                print("✓ Task successfully persisted to database!")
                print(f"   - ID: {persisted_task.id}")
                print(f"   - Title: {persisted_task.title}")
                print(f"   - User ID: {persisted_task.user_id}")
                print(f"   - Completed: {persisted_task.completed}")
                print(f"   - Created: {persisted_task.created_at}")
            else:
                print("✗ Task NOT found in database - data not persisting!")
                return False
    except Exception as e:
        print(f"✗ Data verification failed: {e}")
        return False

    # Step 6: List all tasks for the test user
    print("\n[6] Listing all tasks for test user...")
    try:
        with Session(engine) as session:
            user_tasks = session.exec(
                select(Task).where(Task.user_id == test_user_id)
            ).all()
            print(f"   - Total tasks for test user: {len(user_tasks)}")
            for task in user_tasks[:5]:  # Show first 5
                print(f"     • [{task.id}] {task.title} (completed: {task.completed})")
    except Exception as e:
        print(f"✗ Task listing failed: {e}")
        return False

    print("\n" + "=" * 60)
    print("DIAGNOSTIC COMPLETE - ALL TESTS PASSED!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    print("\nStarting database diagnostic...\n")
    success = test_database_connection()

    if success:
        print("\n✓ Database is working correctly!")
        print("  If data still doesn't appear in your application,")
        print("  the issue may be with JWT authentication or API calls.\n")
        sys.exit(0)
    else:
        print("\n✗ Database issues detected!")
        print("  Please check the error messages above.\n")
        sys.exit(1)
