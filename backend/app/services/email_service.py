from email.message import EmailMessage
import aiosmtplib
from app.config import settings


async def send_contact_email(payload):
    message = EmailMessage()
    message["From"] = settings.SMTP_USER
    message["To"] = settings.OWNER_EMAIL
    message["Subject"] = "New Contact Submission"
    message.set_content(f"""Name: {payload.full_name}
Email: {payload.business_email}
Phone: {payload.phone_number}
Company: {payload.company_name}
Service: {payload.service_of_interest}

Message:
{payload.message}
    """)

    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    )
