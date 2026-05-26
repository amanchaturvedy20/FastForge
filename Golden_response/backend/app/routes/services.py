from datetime import datetime
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Services"])


@router.get("/services")
async def get_services():
    services = [
        {
            "id": 1,
            "title": "Web Development",
            "description": "Modern responsive websites built using clean, optimized HTML5, CSS3, and JavaScript.",
            "icon": "globe",
        },
        {
            "id": 2,
            "title": "Backend APIs",
            "description": "Scalable, high-performance REST APIs designed using FastAPI, Pydantic, and SQLAlchemy.",
            "icon": "server",
        },
        {
            "id": 3,
            "title": "Database Solutions",
            "description": "Robust database design, optimization, and migration workflows using PostgreSQL and SQLite.",
            "icon": "database",
        },
    ]

    return {
        "status": "success",
        "message": "Services retrieved successfully",
        "data": services,
        "timestamp": str(datetime.utcnow()),
    }
