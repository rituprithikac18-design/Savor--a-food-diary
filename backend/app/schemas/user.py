from typing import Optional, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    city: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    city: Optional[str] = None

class UserInDBBase(UserBase):
    user_id: int
    public_id: UUID
    is_verified: bool
    role: str
    taste_profile: Optional[Any] = None
    created_at: datetime

    class Config:
        from_attributes = True

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    password_hash: str
