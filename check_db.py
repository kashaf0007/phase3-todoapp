from backend.database.connection import engine
from backend.src.models.task import Task
from sqlmodel import select
from sqlmodel import Session


with Session(engine) as session:
    # Find tasks for our test user
    user_tasks = session.exec(select(Task).where(Task.user_id == 'debug_test_user')).all()
    print('Tasks for debug_test_user:', len(user_tasks))
    for task in user_tasks:
        print('  - ID:', task.id, 'Title:', task.title)
        
    # Also check all tasks to see what's in the DB
    all_tasks = session.exec(select(Task)).all()
    print('Total tasks in DB:', len(all_tasks))
    for task in all_tasks[-5:]:  # Last 5 tasks
        print('  - ID:', task.id, 'User:', task.user_id, 'Title:', task.title)