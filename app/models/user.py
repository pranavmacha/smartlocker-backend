from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String(128), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=True)
    total_sessions = Column(Integer, default=0)
    total_time = Column(Integer, default=0)  # in minutes
    total_spent = Column(Float, default=0.0)  # in rupees
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    sessions = relationship("LockerSession", back_populates="user")