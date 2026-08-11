from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, restaurants, dishes, reviews

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
api_router.include_router(dishes.router, prefix="/dishes", tags=["dishes"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
