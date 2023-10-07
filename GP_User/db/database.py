from contextlib import contextmanager
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Config

SQLALCHEMY_DATABASE_URI = Config.SQLALCHEMY_DATABASE_URI
engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 建立 Base, 作為後續建立 ORM model 時需要繼承的對象
Base = declarative_base()

# 建立 get_db()
async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()