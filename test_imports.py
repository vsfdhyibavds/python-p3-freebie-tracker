import sys

print("Python executable:", sys.executable)
print("Python sys.path:", sys.path)

try:
    import sqlalchemy
    print("SQLAlchemy imported successfully")
except ImportError:
    print("Failed to import SQLAlchemy")

try:
    import alembic
    print("Alembic imported successfully")
except ImportError:
    print("Failed to import Alembic")
