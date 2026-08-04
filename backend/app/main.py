from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.redis import get_redis

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["health"])
async def health_check():
    redis_client = await get_redis()
    redis_status = "ok"
    try:
        await redis_client.ping()
    except Exception:
        redis_status = "failed"
        
    return {
        "status": "ok",
        "redis": redis_status,
        "api_version": settings.API_V1_STR
    }
