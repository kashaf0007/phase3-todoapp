"""
Debug JWT Token and Database State
Helps identify why data isn't showing up.
"""

import os
import sys

# Load environment
env_file = ".env"
if os.path.exists(env_file):
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ[key] = value

print("=" * 70)
print("JWT & DATABASE DEBUG TOOL")
print("=" * 70)

# Check secrets
better_auth_secret = os.getenv("BETTER_AUTH_SECRET", "")
print(f"\n[1] BETTER_AUTH_SECRET: {better_auth_secret[:20]}... (length: {len(better_auth_secret)})")

if better_auth_secret == "your-secret-here-minimum-32-characters":
    print("    WARNING: Using placeholder secret! JWT verification will fail.")
    print("    Generate a real secret with: openssl rand -base64 32")

# Decode a sample JWT (if provided)
print("\n[2] JWT Token Decoder")
print("    Paste a JWT token from your browser (or press Enter to skip):")
sample_token = input("    Token: ").strip()

if sample_token:
    try:
        from jose import jwt, JWTError

        # Decode without verification first to see payload
        print("\n    [a] Token payload (unverified):")
        unverified = jwt.get_unverified_claims(sample_token)
        for key, value in unverified.items():
            print(f"        {key}: {value}")

        # Now verify with secret
        print("\n    [b] Verifying token with BETTER_AUTH_SECRET...")
        try:
            verified = jwt.decode(sample_token, better_auth_secret, algorithms=["HS256"])
            print("        ✓ Token verification SUCCESSFUL!")
            print(f"        User ID (sub): {verified.get('sub')}")
        except JWTError as e:
            print(f"        X Token verification FAILED: {e}")
            print("        This means:")
            print("          - The BETTER_AUTH_SECRET doesn't match frontend")
            print("          - OR the token is expired")
            print("          - OR the token format is invalid")
    except ImportError:
        print("    python-jose not installed, skipping JWT decode")
    except KeyboardInterrupt:
        print("\n    Skipped.")

# Check database
print("\n[3] Checking database...")
db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("    X DATABASE_URL not set!")
    sys.exit(1)

try:
    import psycopg2

    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    # Check users table
    print("\n    [a] Users in database:")
    cursor.execute("SELECT id, email, created_at FROM users ORDER BY created_at DESC LIMIT 10")
    users = cursor.fetchall()
    if users:
        for user_id, email, created_at in users:
            print(f"        - {user_id[:20]}... ({email}) created {created_at}")
    else:
        print("        (No users found)")
        print("        ^ THIS IS THE PROBLEM! Register a user first!")

    # Check tasks table
    print("\n    [b] Tasks in database:")
    cursor.execute("""
        SELECT t.id, t.user_id, t.title, t.completed, t.created_at
        FROM tasks t
        ORDER BY t.created_at DESC
        LIMIT 10
    """)
    tasks = cursor.fetchall()
    if tasks:
        for task_id, user_id, title, completed, created_at in tasks:
            status = "✓" if completed else " "
            print(f"        [{status}] Task #{task_id}: {title[:40]} (user: {user_id[:10]}...) at {created_at}")
    else:
        print("        (No tasks found)")

    cursor.close()
    conn.close()

    print("\n" + "=" * 70)
    print("DIAGNOSIS:")
    print("=" * 70)

    if not users:
        print("⚠ NO USERS FOUND - You need to register a user first!")
        print("  1. Go to http://localhost:3000/signup")
        print("  2. Create an account")
        print("  3. Try creating tasks again")
    elif not tasks:
        print("⚠ NO TASKS FOUND - Database is working but no tasks created yet.")
        print("  Possible causes:")
        print("  - JWT token verification failing (check secrets match)")
        print("  - API requests not reaching backend")
        print("  - Tasks created under different user_id")
    else:
        print("✓ Database has users AND tasks!")
        print("  If data isn't showing in UI:")
        print("  - Check that JWT token has correct user_id in 'sub' claim")
        print("  - Check browser console for API errors")
        print("  - Verify BETTER_AUTH_SECRET matches between frontend/backend")

except ImportError:
    print("    psycopg2 not installed")
except Exception as e:
    print(f"    X Database error: {e}")

print("\n" + "=" * 70)
