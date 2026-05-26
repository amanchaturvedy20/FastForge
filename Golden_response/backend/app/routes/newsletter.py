from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models.newsletter import Newsletter
from app.schemas.newsletter import NewsletterSchema
from app.routes.contact import limiter
from app.utils.logger import submission_logger


router = APIRouter(prefix="/api", tags=["Newsletter"])


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/newsletter")
@limiter.limit("5/minute")
async def subscribe_newsletter(
    request: Request,
    payload: NewsletterSchema,
    db: AsyncSession = Depends(get_db),
):
    # Check if already subscribed
    result = await db.execute(
        select(Newsletter).where(Newsletter.email == payload.email)
    )
    existing = result.scalars().first()
    if existing:
        return {
            "status": "success",
            "message": "Already subscribed to newsletter",
            "timestamp": str(datetime.utcnow()),
        }

    subscriber = Newsletter(email=payload.email)
    db.add(subscriber)
    await db.commit()

    submission_logger.info(f"Newsletter subscription saved: Email={payload.email}")

    return {
        "status": "success",
        "message": "Successfully subscribed to newsletter",
        "data": {"email": payload.email},
        "timestamp": str(datetime.utcnow()),
    }
