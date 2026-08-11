from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, get_current_active_user, get_current_user
from app.core.rate_limit import general_rate_limiter
from app.models.user import User
from app.schemas.user import User as UserSchema, UserUpdate

router = APIRouter()

@router.get("/me", response_model=UserSchema, dependencies=[Depends(general_rate_limiter)])
async def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    return current_user

@router.put("/me", response_model=UserSchema, dependencies=[Depends(general_rate_limiter)])
async def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    if user_in.email is not None and user_in.email != current_user.email:
        stmt = select(User).where(User.email == user_in.email)
        result = await db.execute(stmt)
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Email already in use")
        current_user.email = user_in.email
        
    if user_in.username is not None and user_in.username != current_user.username:
        stmt = select(User).where(User.username == user_in.username)
        result = await db.execute(stmt)
        if result.scalars().first():
            raise HTTPException(status_code=400, detail="Username already taken")
        current_user.username = user_in.username

    if user_in.bio is not None:
        current_user.bio = user_in.bio
    if user_in.avatar_url is not None:
        current_user.avatar_url = user_in.avatar_url
    if user_in.city is not None:
        current_user.city = user_in.city
    
    # We will compute taste_profile in a background job or periodically, 
    # but we could also mock it here.
    if not current_user.taste_profile:
        current_user.taste_profile = {"favorite_cuisines": [], "price_preference": 2}

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user
