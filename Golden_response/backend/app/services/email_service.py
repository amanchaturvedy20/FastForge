from email.message import EmailMessage
import aiosmtplib
from app.config import settings


async def send_contact_email(payload):
    # 1. Email to Owner
    owner_message = EmailMessage()
    owner_message["From"] = settings.SMTP_USER
    owner_message["To"] = settings.OWNER_EMAIL
    owner_message["Subject"] = "New Contact Submission"
    owner_message.set_content(f"""Name: {payload.full_name}
Email: {payload.business_email}
Phone: {payload.phone_number}
Company: {payload.company_name or 'N/A'}
Service: {payload.service_of_interest or 'N/A'}

Message:
{payload.message}
    """)

    await aiosmtplib.send(
        owner_message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        start_tls=True,
    )

    # 2. Confirmation Email to User
    user_message = EmailMessage()
    user_message["From"] = settings.SMTP_USER
    user_message["To"] = payload.business_email
    user_message["Subject"] = "We received your message!"
    user_message.set_content(f"""Hello {payload.full_name},

Thank you for contacting us. We have successfully received your message and our team will get back to you shortly.

Best regards,
Startup Team
""")

    try:
        await aiosmtplib.send(
            user_message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            start_tls=True,
        )
    except Exception:
        # Ignore error if confirmation email fails, just log it or pass
        pass

