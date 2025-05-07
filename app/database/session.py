from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

#DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Postgres@localhost:5432/trackerapp")
DATABASE_URL = "postgresql://postgres:Postgres@localhost:5432/trackerapp"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base =declarative_base()