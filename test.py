from sqlalchemy import create_engine
#sqlalchemy.url = "postgresql://postgres:Postgres@123@localhost:5432/trackerapp"
engine = create_engine("postgresql://postgres:Postgres@localhost:5432/trackerapp")
with engine.connect() as conn:
    print("Connected successfully!")
from app.database.session import Base
print(Base.metadata.tables.keys())
print(Base._decl_class_registry.items())