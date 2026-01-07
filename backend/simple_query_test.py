"""Simple query test without Unicode characters"""
from src.database import engine
import sqlalchemy

print("Testing database queries...")
print("=" * 60)

with engine.connect() as conn:
    # Count users
    user_count = conn.execute(
        sqlalchemy.text("SELECT COUNT(*) FROM users")
    ).scalar()
    print(f"\nUsers in database: {user_count}")

    # Count tasks
    task_count = conn.execute(
        sqlalchemy.text("SELECT COUNT(*) FROM tasks")
    ).scalar()
    print(f"Tasks in database: {task_count}")

    # Get sample users (limit 5)
    if user_count > 0:
        print("\nSample users:")
        users = conn.execute(
            sqlalchemy.text("SELECT id, email, created_at FROM users LIMIT 5")
        ).fetchall()
        for user in users:
            print(f"  - {user[0][:8]}... | {user[1]} | {user[2]}")

    # Get sample tasks (limit 5)
    if task_count > 0:
        print("\nSample tasks:")
        tasks = conn.execute(
            sqlalchemy.text("SELECT id, title, completed, user_id FROM tasks LIMIT 5")
        ).fetchall()
        for task in tasks:
            print(f"  - [{task[0]}] {task[1]} (completed: {task[2]}) - user: {task[3][:8]}...")

print("\n" + "=" * 60)
print("Database is connected and queryable!")
