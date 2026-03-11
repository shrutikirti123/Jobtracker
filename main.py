from fastapi import FastAPI, Request, Depends, HTTPException
import traceback
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
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc)
        }
    )
@app.get("/health")
def health():

    return {
        "status": "ok",
        "service": "jobtracker-api"
    }

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(job_routes.router, prefix="/jobs", tags=["Jobs"])
app.include_router(resume_routes.router, prefix="/resume", tags=["Resume"])
app.include_router(analytics_routes.router, prefix="/analytics", tags=["Analytics"])