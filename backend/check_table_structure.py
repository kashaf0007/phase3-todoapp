"""Check table structure in the database"""
from src.database import engine
import sqlalchemy

# Connect and query for table structure
with engine.connect() as conn:
    # Check users table structure
    print("=== USERS TABLE STRUCTURE ===")
    users_cols = conn.execute(
        sqlalchemy.text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = 'users'
            ORDER BY ordinal_position
        """)
    ).fetchall()

    for col in users_cols:
        print(f"  {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")

    # Check tasks table structure
    print("\n=== TASKS TABLE STRUCTURE ===")
    tasks_cols = conn.execute(
        sqlalchemy.text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = 'tasks'
            ORDER BY ordinal_position
        """)
    ).fetchall()

    for col in tasks_cols:
        print(f"  {col[0]}: {col[1]} (nullable: {col[2]}, default: {col[3]})")

    # Check foreign keys
    print("\n=== FOREIGN KEYS ===")
    fks = conn.execute(
        sqlalchemy.text("""
            SELECT
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
                ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY'
                AND tc.table_schema = 'public'
                AND tc.table_name IN ('users', 'tasks')
        """)
    ).fetchall()

    for fk in fks:
        print(f"  {fk[0]}.{fk[1]} -> {fk[2]}.{fk[3]}")

    # Check indexes
    print("\n=== INDEXES ===")
    indexes = conn.execute(
        sqlalchemy.text("""
            SELECT
                tablename,
                indexname,
                indexdef
            FROM pg_indexes
            WHERE schemaname = 'public'
                AND tablename IN ('users', 'tasks')
            ORDER BY tablename, indexname
        """)
    ).fetchall()

    for idx in indexes:
        print(f"  {idx[0]}.{idx[1]}")
        print(f"    {idx[2]}")
