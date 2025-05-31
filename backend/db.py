from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import (
    SQL_DATABASE_URI,
)  # e.g., "postgresql+psycopg2://postgres:password@localhost:5432/yourdbname"

# Create the SQLAlchemy engine (connection pooling is handled here)
engine = create_engine(SQL_DATABASE_URI, pool_size=10, max_overflow=0, echo=False)

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
