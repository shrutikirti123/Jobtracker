from fastapi import FastAPI
from slowapi.util import get_remote_address
from database import Base, engine
import os
from routes import auth_routes, job_routes, resume_routes
from core.limiter import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from routes import analytics_routes

app = FastAPI()

os.makedirs("resumes", exist_ok=True)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)
@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(job_routes.router, prefix="/jobs", tags=["Jobs"])
app.include_router(resume_routes.router, prefix="/resume", tags=["Resume"])
app.include_router(analytics_routes.router, prefix="/analytics", tags=["Analytics"])