from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

class DishBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None

class DishCreate(DishBase):
    pass

class DishUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class DishInDBBase(DishBase):
    dish_id: int
    public_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class Dish(DishInDBBase):
    pass

# RestaurantDish Schemas
class RestaurantDishBase(BaseModel):
    price: Optional[float] = None

class RestaurantDishCreate(RestaurantDishBase):
    restaurant_id: int
    dish_id: int

class RestaurantDishUpdate(BaseModel):
    price: Optional[float] = None

class RestaurantDishInDBBase(RestaurantDishBase):
    restaurant_dish_id: int
    restaurant_id: int
    dish_id: int
    love_count: int
    avg_rating: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True

class RestaurantDish(RestaurantDishInDBBase):
    pass
