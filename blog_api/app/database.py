import sqlalchemy
from models import Base
from sqlalchemy.orm import sessionmaker, declarative_base

engine = sqlalchemy.create_engine("sqlite:///test.db", connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
Base.metadata.create_all(bind = engine)