from datetime import datetime
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal
from app.models.contact import Contact
from app.schemas.contact import ContactSchema
from app.services.email_service import send_contact_email

router = APIRouter(prefix="/api", tags=["Contact"])
limiter = Limiter(key_func=get_remote_address)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.post("/contact")
@limiter.limit("5/minute")
async def submit_contact_form(
    request: Request,
    payload: ContactSchema,
    db: AsyncSession = Depends(get_db),
):
    if payload.honeypot:
        return {
            "status": "success",
            "message": "Spam blocked",
            "timestamp": str(datetime.utcnow()),
        }

    contact = Contact(
        full_name=payload.full_name,
        business_email=payload.business_email,
        phone_number=payload.phone_number,
        company_name=payload.company_name,
        service_of_interest=payload.service_of_interest,
        message=payload.message,
    )

    db.add(contact)
    await db.commit()

    try:
        await send_contact_email(payload)
    except Exception:
        pass

    return {
        "status": "success",
        "message": "Form submitted successfully",
        "data": payload.model_dump(),
        "timestamp": str(datetime.utcnow()),
    }
