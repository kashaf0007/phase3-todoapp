"""Simple database test without imports"""
import os
import sys

print("=" * 60)
print("SIMPLE DATABASE TEST")
print("=" * 60)

# Check environment
print("\n[1] Checking environment...")
print(f"   Python: {sys.version}")
print(f"   Working directory: {os.getcwd()}")

# Load .env manually
print("\n[2] Loading environment variables...")
env_file = ".env"
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value

db_url = os.getenv("DATABASE_URL")
if db_url:
    # Hide password in output
    safe_url = db_url.split("@")[0].split(":")[0] + ":***@" + db_url.split("@")[1] if "@" in db_url else "***"
    print(f"   DATABASE_URL found: {safe_url}")
else:
    print("   ✗ DATABASE_URL not found!")
    sys.exit(1)

# Try psycopg2 connection
print("\n[3] Testing raw PostgreSQL connection...")
try:
    import psycopg2
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"   ✓ Connected! PostgreSQL version: {version[0][:50]}...")

    # Check if tables exist
    cursor.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    print(f"\n[4] Existing tables in database:")
    if tables:
        for table in tables:
            print(f"      - {table[0]}")
    else:
        print("      (No tables found)")

    cursor.close()
    conn.close()
    print("\n   ✓ Database connection test passed!")

except Exception as e:
    print(f"   ✗ Connection failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
