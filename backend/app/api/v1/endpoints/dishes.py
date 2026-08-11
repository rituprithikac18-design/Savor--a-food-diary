from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, get_current_active_user, RequireRole
from app.core.rate_limit import general_rate_limiter
from app.models.dish import Dish, RestaurantDish
from app.models.restaurant import Restaurant
from app.models.user import User
from app.schemas.dish import Dish as DishSchema, DishCreate, DishUpdate, RestaurantDish as RestaurantDishSchema, RestaurantDishCreate

router = APIRouter()

@router.get("/", response_model=List[DishSchema], dependencies=[Depends(general_rate_limiter)])
async def read_dishes(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    stmt = select(Dish).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/", response_model=DishSchema, dependencies=[Depends(RequireRole(["restaurant_owner"]))])
async def create_dish(
    *,
    db: AsyncSession = Depends(get_db),
    dish_in: DishCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    dish = Dish(
        name=dish_in.name,
        description=dish_in.description,
        category=dish_in.category,
    )
    db.add(dish)
    await db.commit()
    await db.refresh(dish)
    return dish

@router.post("/restaurant-dish", response_model=RestaurantDishSchema, dependencies=[Depends(RequireRole(["restaurant_owner"]))])
async def add_dish_to_restaurant(
    *,
    db: AsyncSession = Depends(get_db),
    rd_in: RestaurantDishCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    restaurant = await db.get(Restaurant, rd_in.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    if restaurant.created_by != current_user.user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
        
    rd = RestaurantDish(
        restaurant_id=rd_in.restaurant_id,
        dish_id=rd_in.dish_id,
        price=rd_in.price,
    )
    db.add(rd)
    await db.commit()
    await db.refresh(rd)
    return rd
