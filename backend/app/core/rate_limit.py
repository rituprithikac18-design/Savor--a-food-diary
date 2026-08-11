from fastapi import Request, HTTPException, status
import time
from app.db.redis import get_redis

class RateLimiter:
    def __init__(self, requests: int, window: int):
        self.requests = requests
        self.window = window

    async def __call__(self, request: Request):
        # Use client IP as the identifier, or use user ID if authenticated
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            client_ip = forwarded.split(",")[0]
        else:
            client_ip = request.client.host if request.client else "127.0.0.1"

        path = request.url.path
        # Group routes for rate limiting
        route_group = "auth" if path.startswith("/api/v1/auth") else "general"
        
        # We can dynamically adjust limits based on the route group if we wanted to
        # but the instances of RateLimiter will be attached to specific routers
        
        key = f"rate_limit:{route_group}:{client_ip}"
        
        redis_client = await get_redis()
        
        current_time = int(time.time())
        window_start = current_time - self.window
        
        # Sliding window approach using Redis ZSET
        async with redis_client.pipeline(transaction=True) as pipe:
            pipe.zremrangebyscore(key, 0, window_start)
            pipe.zcard(key)
            pipe.zadd(key, {str(current_time): current_time})
            pipe.expire(key, self.window)
            results = await pipe.execute()
            
        request_count = results[1]
        
        if request_count >= self.requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests, please try again later."
            )

# 10 requests per minute
auth_rate_limiter = RateLimiter(requests=10, window=60)
# 300 requests per minute
general_rate_limiter = RateLimiter(requests=300, window=60)
