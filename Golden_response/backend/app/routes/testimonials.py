from datetime import datetime
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["Testimonials"])


@router.get("/testimonials")
async def get_testimonials():
    testimonials = [
        {
            "id": 1,
            "name": "Sarah Connor",
            "designation": "CEO, TechInnovate",
            "feedback": "FastForge built our landing page and backend in record time. The performance is outstanding!",
        },
        {
            "id": 2,
            "name": "John Doe",
            "designation": "Founder, ShopSphere",
            "feedback": "Using FastAPI and Vanilla JS was the best decision. No framework bloat, just speed and reliability.",
        },
        {
            "id": 3,
            "name": "Elena Rostova",
            "designation": "Product Manager, ApexCorp",
            "feedback": "The contact forms, email alerts, and dockerized deployment worked flawlessly right out of the box.",
        },
    ]

    return {
        "status": "success",
        "message": "Testimonials retrieved successfully",
        "data": testimonials,
        "timestamp": str(datetime.utcnow()),
    }
