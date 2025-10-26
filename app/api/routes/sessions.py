from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.models.user import User
from app.models.locker_session import LockerSession
from app.schemas.session import SessionCreate, SessionEnd, SessionOut

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/start", response_model=SessionOut)
def start_session(payload: SessionCreate, db: Session = Depends(get_db)):
    """Start a new charging session"""
    user = db.query(User).filter(User.firebase_uid == payload.firebase_uid).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create session
    session = LockerSession(
        user_id=user.id,
        start_time=payload.start_time,
        duration_minutes=payload.duration_minutes,
        amount_paid=payload.amount_paid,
        is_active=True,
        status="active"
    )
    
    # Update user stats
    user.total_sessions += 1
    user.total_time += payload.duration_minutes
    user.total_spent += payload.amount_paid
    
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return session

@router.post("/{session_id}/end", response_model=SessionOut)
def end_session(session_id: int, payload: SessionEnd, db: Session = Depends(get_db)):
    """End a charging session"""
    session = db.query(LockerSession).filter(LockerSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.is_active:
        raise HTTPException(status_code=400, detail="Session already ended")
    
    # Update session
    session.end_time = datetime.utcnow()
    session.overtime_minutes = payload.overtime_minutes
    session.overtime_charge = payload.overtime_charge
    session.is_active = False
    session.status = "completed"
    
    # Update user stats if overtime
    if payload.overtime_minutes > 0:
        user = session.user
        user.total_time += payload.overtime_minutes
        user.total_spent += payload.overtime_charge
    
    db.commit()
    db.refresh(session)
    
    return session

@router.get("/user/{firebase_uid}", response_model=List[SessionOut])
def get_user_sessions(firebase_uid: str, db: Session = Depends(get_db)):
    """Get all sessions for a user"""
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    sessions = db.query(LockerSession).filter(LockerSession.user_id == user.id).order_by(LockerSession.start_time.desc()).all()
    
    return sessions