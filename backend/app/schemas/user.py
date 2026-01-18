from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    preferred_categories: Optional[List[str]] = None
    preferred_sources: Optional[List[str]] = None
    min_quality_score: Optional[int] = None
    email_frequency: Optional[str] = None
    email_enabled: Optional[bool] = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: Optional[str] = None
    preferred_categories: List[str] = []
    preferred_sources: List[str] = []
    min_quality_score: int = 60
    email_frequency: str = "daily"
    email_enabled: bool = True
    is_active: bool = True
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
