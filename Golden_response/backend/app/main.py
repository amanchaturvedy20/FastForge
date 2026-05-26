import time
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.config import settings
from app.routes.contact import router as contact_router
from app.routes.health import router as health_router
from app.routes.newsletter import router as newsletter_router
from app.routes.testimonials import router as testimonials_router
from app.routes.services import router as services_router
from app.utils.logger import app_logger, error_logger




@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import engine, Base
    import app.models
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


from app.routes.contact import limiter as contact_limiter

app = FastAPI(
    title="Startup Website API",
    version="1.0.0",
    lifespan=lifespan,
)
app.state.limiter = contact_limiter

origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(SlowAPIMiddleware)


@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 4)
    app_logger.info(
        f"{request.method} {request.url.path} "
        f"{response.status_code} {duration}s"
    )
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    error_logger.exception("Unhandled server error: %s", str(exc))
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "Unexpected server error",
            "details": {},
        },
    )


@app.exception_handler(RateLimitExceeded)
async def ratelimit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={
            "status": "error",
            "error_code": "RATE_LIMIT_EXCEEDED",
            "message": "Too many requests",
            "details": {},
        },
    )


app.include_router(contact_router)
app.include_router(health_router)
app.include_router(newsletter_router)
app.include_router(testimonials_router)
app.include_router(services_router)
