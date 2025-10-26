from pydantic import BaseModel, EmailStr
from typing import Optional
from pydantic import EmailStr


class UserCreate(BaseModel):
    firebase_uid: str
    email: EmailStr
    name: Optional[str] = None

class UserStats(BaseModel):
    total_sessions: int
    total_time: int
    total_spent: float

class UserOut(BaseModel):
    id: int
    firebase_uid: str
    email: str
    name: Optional[str]
    total_sessions: int
    total_time: int
    total_spent: float
    
    class Config:
        from_attributes = True