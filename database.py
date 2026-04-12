from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

db_url="postgresql://postgres:12345@localhost:5432/sabbir"
engine=create_engine(db_url)
SessionLocal=sessionmaker(autocommit=False, autoflush=False,bind=engine )