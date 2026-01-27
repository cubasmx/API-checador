from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CheckInBase(BaseModel):
    notes: Optional[str] = None

class CheckInCreate(CheckInBase):
    employee_id: int

class CheckOutCreate(BaseModel):
    notes: Optional[str] = None

class CheckIn(CheckInBase):
    id: int
    employee_id: int
    check_in_time: datetime
    check_out_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
