from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Define the base class for declarative models
Base = declarative_base()

# database connection string
DATABASE_URL = "sqlite:///monster-game.db"
# Create the database engine
engine = create_engine("sqlite:///monster-game.db", echo=True)
# Create a session factory
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)