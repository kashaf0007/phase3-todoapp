"""
Verify all Python modules can be imported successfully
"""
import sys

print("=" * 80)
print("BACKEND MODULE IMPORT CHECK")
print("=" * 80)

modules_to_check = [
    ("src.config", "Configuration"),
    ("src.database", "Database Engine"),
    ("src.models.user", "User Model"),
    ("src.models.task", "Task Model"),
    ("src.api.dependencies", "API Dependencies"),
    ("src.api.routes.health", "Health Routes"),
    ("src.api.routes.auth", "Auth Routes"),
    ("src.api.routes.tasks", "Task Routes"),
    ("src.main", "Main Application"),
]

failed = []
passed = []

for module_name, description in modules_to_check:
    try:
        __import__(module_name)
        print(f"✓ {description:.<50} OK")
        passed.append(module_name)
    except Exception as e:
        print(f"✗ {description:.<50} FAILED")
        print(f"  Error: {e}")
        failed.append((module_name, str(e)))

print("\n" + "=" * 80)
print(f"Results: {len(passed)} passed, {len(failed)} failed")
print("=" * 80)

if failed:
    print("\nFailed imports:")
    for module, error in failed:
        print(f"  - {module}: {error}")
    sys.exit(1)
else:
    print("\n✅ All backend modules imported successfully!")
    print("Backend is ready for deployment.")
    sys.exit(0)
