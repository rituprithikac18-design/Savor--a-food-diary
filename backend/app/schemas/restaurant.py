from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

class RestaurantBase(BaseModel):
    name: str
    address: str
    city: str
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)
    cuisine_tags: Optional[List[str]] = []

class RestaurantCreate(RestaurantBase):
    pass

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    lat: Optional[float] = Field(None, ge=-90, le=90)
    lng: Optional[float] = Field(None, ge=-180, le=180)
    cuisine_tags: Optional[List[str]] = None
    approved: Optional[bool] = None

class RestaurantInDBBase(RestaurantBase):
    restaurant_id: int
    public_id: UUID
    avg_rating: Optional[float] = None
    created_by: Optional[int] = None
    approved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Restaurant(RestaurantInDBBase):
    pass
