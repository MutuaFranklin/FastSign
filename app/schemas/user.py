from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str
    confirm_password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    is_active: bool

    class Config:
        orm_mode = True 