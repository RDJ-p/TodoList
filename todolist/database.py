from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "postgresql://postgres:15975321@localhost:5432/todolist"
engine = create_engine(DATABASE_URL)
Base=declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)