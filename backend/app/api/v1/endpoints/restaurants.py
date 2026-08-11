from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, get_current_active_user, RequireRole
from app.core.rate_limit import general_rate_limiter
from app.models.restaurant import Restaurant
from app.models.user import User
from app.schemas.restaurant import Restaurant as RestaurantSchema, RestaurantCreate, RestaurantUpdate

router = APIRouter()

@router.get("/", response_model=List[RestaurantSchema], dependencies=[Depends(general_rate_limiter)])
async def read_restaurants(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    stmt = select(Restaurant).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=RestaurantSchema, dependencies=[Depends(RequireRole(["restaurant_owner"]))])
async def create_restaurant(
    *,
    db: AsyncSession = Depends(get_db),
    restaurant_in: RestaurantCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    restaurant = Restaurant(
        name=restaurant_in.name,
        address=restaurant_in.address,
        city=restaurant_in.city,
        lat=restaurant_in.lat,
        lng=restaurant_in.lng,
        cuisine_tags=restaurant_in.cuisine_tags,
        created_by=current_user.user_id,
        approved=False # Requires admin approval
    )
    db.add(restaurant)
    await db.commit()
    await db.refresh(restaurant)
    return restaurant

@router.get("/{restaurant_id}", response_model=RestaurantSchema, dependencies=[Depends(general_rate_limiter)])
async def read_restaurant(
    restaurant_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    restaurant = await db.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurant

@router.put("/{restaurant_id}", response_model=RestaurantSchema, dependencies=[Depends(RequireRole(["restaurant_owner"]))])
async def update_restaurant(
    *,
    db: AsyncSession = Depends(get_db),
    restaurant_id: int,
    restaurant_in: RestaurantUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    restaurant = await db.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.created_by != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    update_data = restaurant_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(restaurant, field, value)
        
    db.add(restaurant)
    await db.commit()
    await db.refresh(restaurant)
    return restaurant
