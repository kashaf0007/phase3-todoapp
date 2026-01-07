"""Check what tables exist in the database"""
from src.database import engine
import sqlalchemy

# Connect and query for tables
with engine.connect() as conn:
    result = conn.execute(
        sqlalchemy.text(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"
        )
    ).fetchall()

    print("Tables in public schema:")
    if result:
        for row in result:
            print(f"  - {row[0]}")
    else:
        print("  No tables found!")

    # Also check what schema we're connected to
    schema_result = conn.execute(sqlalchemy.text("SELECT current_schema()")).fetchone()
    print(f"\nCurrent schema: {schema_result[0]}")

    # List all schemas
    schemas = conn.execute(
        sqlalchemy.text("SELECT schema_name FROM information_schema.schemata")
    ).fetchall()
    print("\nAvailable schemas:")
    for schema in schemas:
        print(f"  - {schema[0]}")

