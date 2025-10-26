from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class LockerSession(Base):
    __tablename__ = "locker_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    
    duration_minutes = Column(Integer, nullable=False)
    amount_paid = Column(Float, nullable=False)
    
    overtime_minutes = Column(Integer, default=0)
    overtime_charge = Column(Float, default=0.0)
    
    is_active = Column(Boolean, default=True)
    status = Column(String(50), default="active")  # active/completed/expired
    
    # Relationship
    user = relationship("User", back_populates="sessions")