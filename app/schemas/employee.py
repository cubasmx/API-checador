from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    employee_id: str
    department: Optional[str] = None
    position: Optional[str] = None

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    position: Optional[str] = None
    is_active: Optional[bool] = None

class Employee(EmployeeBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
