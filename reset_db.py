from models.base import Base
from db import engine

# ⚠️ This deletes all existing tables and recreates them
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

print("Database reset complete.")