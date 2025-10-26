from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SessionCreate(BaseModel):
    firebase_uid: str
    duration_minutes: int
    amount_paid: float
    start_time: datetime

class SessionEnd(BaseModel):
    overtime_minutes: int = 0
    overtime_charge: float = 0.0

class SessionOut(BaseModel):
    id: int
    user_id: int
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: int
    amount_paid: float
    overtime_minutes: int
    overtime_charge: float
    is_active: bool
    status: str
    
    class Config:
        from_attributes = True