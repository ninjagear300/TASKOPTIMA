from sqlalchemy import Column, Integer, String, DateTime, Boolean
from .database import Base
from datetime import datetime
from .database import engine

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    priority = Column(Integer)
    deadline = Column(String)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    response = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)
