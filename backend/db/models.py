from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class ScreeningHistory(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_text = Column(Text)
    score = Column(String)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)