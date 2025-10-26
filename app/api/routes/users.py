from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut, UserStats

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/sync", response_model=UserOut)
def sync_user(payload: UserCreate, db: Session = Depends(get_db)):
    """Sync Firebase user to database"""
    user = db.query(User).filter(User.firebase_uid == payload.firebase_uid).first()
    
    if not user:
        user = User(
            firebase_uid=payload.firebase_uid,
            email=payload.email,
            name=payload.name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user

@router.get("/{firebase_uid}/stats", response_model=UserStats)
def get_user_stats(firebase_uid: str, db: Session = Depends(get_db)):
    """Get user statistics"""
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserStats(
        total_sessions=user.total_sessions,
        total_time=user.total_time,
        total_spent=user.total_spent
    )

@router.get("/{firebase_uid}/profile", response_model=UserOut)
def get_user_profile(firebase_uid: str, db: Session = Depends(get_db)):
    """Get complete user profile"""
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user