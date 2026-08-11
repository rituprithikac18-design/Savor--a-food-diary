from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_db, get_current_user
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.core.rate_limit import auth_rate_limiter
from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.token import Token

router = APIRouter()

@router.post("/register", response_model=UserSchema, dependencies=[Depends(auth_rate_limiter)])
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)) -> Any:
    # Check if user exists
    stmt = select(User).where((User.email == user_in.email) | (User.username == user_in.username))
    result = await db.execute(stmt)
    if result.scalars().first():
        raise HTTPException(
            status_code=400,
            detail="The user with this username or email already exists in the system.",
        )
    
    user = User(
        email=user_in.email,
        username=user_in.username,
        password_hash=get_password_hash(user_in.password),
        bio=user_in.bio,
        avatar_url=user_in.avatar_url,
        city=user_in.city,
        is_verified=False, # Wait for email verification
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Mock Email Verification
    print(f"MOCK EMAIL: Please verify your email for user {user.username}. Token: mock_token_123")
    
    return user

@router.post("/login", response_model=Token, dependencies=[Depends(auth_rate_limiter)])
async def login(
    db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    stmt = select(User).where(User.username == form_data.username)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
        
    return {
        "access_token": create_access_token(user.user_id),
        "refresh_token": create_refresh_token(user.user_id),
        "token_type": "bearer",
    }

@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)) -> Any:
    # In a real app we'd blacklist the token in Redis
    return {"msg": "Successfully logged out"}

@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(get_current_user)
) -> Any:
    # We'd typically expect a refresh token here, but for simplicity we'll just issue a new access token
    # assuming the user passed the `get_current_user` dependency (meaning they have a valid token)
    return {
        "access_token": create_access_token(current_user.user_id),
        "token_type": "bearer",
    }
