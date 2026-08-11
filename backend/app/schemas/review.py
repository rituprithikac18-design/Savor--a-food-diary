from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    text: Optional[str] = None
    tags: Optional[List[str]] = []
    photo_urls: Optional[List[str]] = []

class ReviewCreate(ReviewBase):
    restaurant_dish_id: int

class ReviewUpdate(BaseModel):
    rating: Optional[int] = Field(None, ge=1, le=5)
    text: Optional[str] = None
    tags: Optional[List[str]] = None
    photo_urls: Optional[List[str]] = None

class ReviewInDBBase(ReviewBase):
    review_id: int
    public_id: UUID
    user_id: int
    restaurant_dish_id: int
    sentiment_score: Optional[float] = None
    is_deleted: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Review(ReviewInDBBase):
    pass
