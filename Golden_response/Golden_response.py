"""
Golden_response.py
==================
A fully self-contained single-file deployment of the FastForge startup website.
This file consolidates the entire application stack:
- FastAPI Backend API
- SQLite Database (SQLAlchemy Async ORM)
- SlowAPI Rate Limiting & Custom Logger
- Embedded Frontend (HTML, CSS, JS) served directly from FastAPI

To run this file:
1. Install dependencies:
   pip install fastapi "uvicorn[standard]" sqlalchemy asyncpg aiosqlite pydantic pydantic-settings python-dotenv slowapi aiosmtplib email-validator
2. Run the script:
   python Golden_response.py
3. Open your browser at:
   http://127.0.0.1:8000
"""

import logging
import os
import time
from contextlib import asynccontextmanager
from datetime import datetime
from email.message import EmailMessage
from typing import Optional

import aiosmtplib
import uvicorn
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic_settings import BaseSettings
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from sqlalchemy import String, DateTime, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# ==========================================
# 1. CONFIGURATION & ENVIRONMENT SETTINGS
# ==========================================
class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./startup.db"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = "example@gmail.com"
    SMTP_PASSWORD: str = "password"
    OWNER_EMAIL: str = "owner@example.com"
    SECRET_API_KEY: str = "secret"
    ALLOWED_ORIGINS: str = "http://localhost:5500,http://127.0.0.1:5500,http://localhost:8000,http://127.0.0.1:8000"
    ENVIRONMENT: str = "development"

    model_config = ConfigDict(env_file=".env", extra="ignore")

settings = Settings()

# ==========================================
# 2. LOGGING CONFIGURATION
# ==========================================
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')

def setup_logger(name, log_file, level=logging.INFO):
    handler = logging.FileHandler(os.path.join(LOG_DIR, log_file))
    handler.setFormatter(formatter)
    
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger

app_logger = setup_logger("app", "app.log")
error_logger = setup_logger("error", "errors.log", level=logging.ERROR)
submission_logger = setup_logger("submissions", "submissions.log")

# ==========================================
# 3. DATABASE MODELS & SETUP
# ==========================================
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(255))
    business_email: Mapped[str] = mapped_column(String(255))
    phone_number: Mapped[str] = mapped_column(String(100))
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    service_of_interest: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    message: Mapped[str] = mapped_column(String(5000))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Newsletter(Base):
    __tablename__ = "newsletter_subscribers"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    subscribed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ==========================================
# 4. PYDANTIC SCHEMAS
# ==========================================
class ContactSchema(BaseModel):
    full_name: str = Field(min_length=2, max_length=255)
    business_email: EmailStr
    phone_number: str = Field(min_length=7, max_length=20)
    company_name: Optional[str] = None
    service_of_interest: Optional[str] = None
    message: str = Field(min_length=10, max_length=5000)
    honeypot: Optional[str] = None

    model_config = ConfigDict(str_strip_whitespace=True)

class NewsletterSchema(BaseModel):
    email: EmailStr

    model_config = ConfigDict(str_strip_whitespace=True)

# ==========================================
# 5. ASYNC EMAIL SERVICE
# ==========================================
async def send_contact_email(payload: ContactSchema):
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
        # Ignore user receipt failure, logging only
        pass

# ==========================================
# 6. LIFESPAN MANAGEMENT
# ==========================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform database table creation
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

# ==========================================
# 7. FASTAPI APPLICATION SETUP
# ==========================================
limiter = Limiter(key_func=get_remote_address)
app = FastAPI(
    title="Startup Website API",
    version="1.0.0",
    lifespan=lifespan,
)
app.state.limiter = limiter

origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SlowAPIMiddleware)

# Logger Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = round(time.time() - start, 4)
    app_logger.info(f"{request.method} {request.url.path} {response.status_code} {duration}s")
    return response

# Error Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
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
async def ratelimit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "status": "error",
            "error_code": "RATE_LIMIT_EXCEEDED",
            "message": "Too many requests",
            "details": {},
        },
    )

# ==========================================
# 8. BACKEND API ENDPOINTS
# ==========================================
@app.get("/api/health", tags=["Health"])
async def health_check():
    return {
        "status": "success",
        "message": "API healthy",
        "timestamp": str(datetime.utcnow()),
    }

@app.get("/api/services", tags=["Services"])
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

@app.get("/api/testimonials", tags=["Testimonials"])
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

@app.post("/api/contact", tags=["Contact"])
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

    submission_logger.info(f"Contact form submission saved: Name={payload.full_name}, Email={payload.business_email}")

    try:
        await send_contact_email(payload)
        submission_logger.info(f"Email notification sent successfully for contact: {payload.business_email}")
    except Exception as e:
        submission_logger.error(f"Email notification failed for contact: {payload.business_email}. Error: {str(e)}")

    return {
        "status": "success",
        "message": "Form submitted successfully",
        "data": payload.model_dump(),
        "timestamp": str(datetime.utcnow()),
    }

@app.post("/api/newsletter", tags=["Newsletter"])
@limiter.limit("5/minute")
async def subscribe_newsletter(
    request: Request,
    payload: NewsletterSchema,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Newsletter).where(Newsletter.email == payload.email))
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

# ==========================================
# 9. EMBEDDED FRONTEND RESOURCES
# ==========================================

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Startup</title>
    <meta name="description" content="Fast modern startup website">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="stylesheet" href="/css/responsive.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="/js/main.js" defer></script>
    <script src="/js/form.js" defer></script>
</head>
<body>
    <header class="header">
        <nav class="navbar container">
            <div class="logo">Startup</div>
            <button id="hamburger">☰</button>
            <ul id="nav-links">
                <li><a href="#hero">Home</a></li>
                <li><a href="#services">Services</a></li>
                <li><a href="#testimonials">Testimonials</a></li>
                <li><a href="#contact">Contact</a></li>
            </ul>
        </nav>
    </header>

    <section id="hero" class="hero fade-in">
        <div class="container">
            <h1>Modern FastAPI Startup Website</h1>
            <p>Production-ready responsive business solution.</p>
            <a href="#contact" class="btn">Book Demo</a>
        </div>
    </section>

    <section id="services" class="fade-in">
        <div class="container">
            <h2>Services</h2>
            <div id="services-grid" class="grid">
                <!-- Loaded dynamically -->
            </div>
        </div>
    </section>

    <section id="testimonials" class="fade-in">
        <div class="container">
            <h2>What Our Clients Say</h2>
            <div id="testimonials-grid" class="grid">
                <!-- Loaded dynamically -->
            </div>
        </div>
    </section>

    <section id="contact" class="fade-in">
        <div class="container">
            <h2>Contact</h2>
            <form id="contact-form">
                <input type="text" name="honeypot" hidden>
                <input type="text" name="full_name" placeholder="Full Name" required>
                <input type="email" name="business_email" placeholder="Business Email" required>
                <input type="text" name="phone_number" placeholder="Phone Number" required>
                <textarea name="message" placeholder="Message"></textarea>
                <button type="submit" class="btn">Send</button>
            </form>
            <div id="form-message"></div>
        </div>
    </section>
</body>
</html>
"""

STYLE_CSS = """:root {
    --primary: #2563eb;
    --dark: #0f172a;
    --light: #ffffff;
    --gray: #64748b;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: #f8fafc;
    color: var(--dark);
}

.container {
    width: 90%;
    max-width: 1200px;
    margin: auto;
}

.header {
    position: sticky;
    top: 0;
    background: white;
    padding: 20px 0;
    z-index: 100;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary);
}

#hamburger {
    display: none;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
}

#nav-links {
    list-style: none;
    display: flex;
    gap: 20px;
}

#nav-links a {
    text-decoration: none;
    color: var(--dark);
    font-weight: 500;
    transition: color 0.3s ease;
}

#nav-links a:hover {
    color: var(--primary);
}

.hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
}

.hero h1 {
    font-size: 2.5rem;
    margin-bottom: 16px;
}

.hero p {
    font-size: 1.2rem;
    color: var(--gray);
    margin-bottom: 24px;
}

.grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.card h3 {
    margin-bottom: 8px;
    color: var(--primary);
}

.card p {
    color: var(--gray);
}

.btn {
    display: inline-block;
    padding: 14px 24px;
    background: var(--primary);
    color: white;
    text-decoration: none;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 1rem;
    transition: background 0.3s ease, transform 0.2s ease;
}

.btn:hover {
    background: #1d4ed8;
    transform: translateY(-2px);
}

section {
    padding: 80px 0;
}

section h2 {
    font-size: 2rem;
    margin-bottom: 32px;
    text-align: center;
}

#contact-form {
    max-width: 600px;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

#contact-form input,
#contact-form textarea {
    padding: 14px;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease;
}

#contact-form input:focus,
#contact-form textarea:focus {
    outline: none;
    border-color: var(--primary);
}

#contact-form textarea {
    min-height: 120px;
    resize: vertical;
}

#form-message {
    text-align: center;
    margin-top: 16px;
    font-weight: 500;
    color: var(--primary);
}

.fade-in {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.5s ease;
}

.fade-in.show {
    opacity: 1;
    transform: translateY(0);
}
"""

RESPONSIVE_CSS = """@media (max-width: 768px) {
    #hamburger {
        display: block;
    }

    #nav-links {
        display: none;
        flex-direction: column;
        position: absolute;
        top: 60px;
        right: 5%;
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        gap: 12px;
    }

    #nav-links.active {
        display: flex;
    }

    .hero h1 {
        font-size: 1.8rem;
    }

    .hero p {
        font-size: 1rem;
    }
}
"""

MAIN_JS = """const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show");
        }
    });
});

const sections = document.querySelectorAll(".fade-in");
sections.forEach((section) => {
    observer.observe(section);
});

const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("nav-links");

if (hamburger && navLinks) {
    hamburger.addEventListener("click", () => {
        navLinks.classList.toggle("active");
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadServices();
    loadTestimonials();
});

async function loadServices() {
    const grid = document.getElementById("services-grid");
    if (!grid) return;

    try {
        const response = await fetch('/api/services');
        const result = await response.json();

        if (result.status === "success" && Array.isArray(result.data)) {
            grid.innerHTML = result.data.map(service => `
                <div class="card">
                    <div style="font-size: 2rem; margin-bottom: 12px; color: var(--primary);">
                        <i class="fa fa-${service.icon || 'cogs'}"></i>
                    </div>
                    <h3>${service.title}</h3>
                    <p>${service.description}</p>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error("Error loading services:", error);
        grid.innerHTML = `<p>Error loading services. Please try again later.</p>`;
    }
}

async function loadTestimonials() {
    const grid = document.getElementById("testimonials-grid");
    if (!grid) return;

    try {
        const response = await fetch('/api/testimonials');
        const result = await response.json();

        if (result.status === "success" && Array.isArray(result.data)) {
            grid.innerHTML = result.data.map(testimonial => `
                <div class="card">
                    <p style="font-style: italic; margin-bottom: 16px;">"${testimonial.feedback}"</p>
                    <h4 style="color: var(--primary); font-weight: bold;">${testimonial.name}</h4>
                    <span style="font-size: 0.85rem; color: var(--gray);">${testimonial.designation}</span>
                </div>
            `).join('');
        }
    } catch (error) {
        console.error("Error loading testimonials:", error);
        grid.innerHTML = `<p>Error loading testimonials. Please try again later.</p>`;
    }
}
"""

FORM_JS = """const form = document.getElementById("contact-form");
const message = document.getElementById("form-message");

if (form) {
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);
        const payload = {
            full_name: formData.get("full_name"),
            business_email: formData.get("business_email"),
            phone_number: formData.get("phone_number"),
            message: formData.get("message"),
            honeypot: formData.get("honeypot"),
        };

        try {
            const response = await fetch('/api/contact', {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            const result = await response.json();

            if (response.ok) {
                message.innerText = result.message;
                form.reset();
            } else {
                message.innerText = result.message || "Submission failed";
            }
        } catch (error) {
            message.innerText = "Server error";
        }
    });
}
"""

# ==========================================
# 10. FRONTEND ROUTINGS (SERVED BY FASTAPI)
# ==========================================
@app.get("/", response_class=HTMLResponse, tags=["Frontend"])
async def get_index():
    return HTMLResponse(content=INDEX_HTML)

@app.get("/css/style.css", tags=["Frontend"])
async def get_style():
    return Response(content=STYLE_CSS, media_type="text/css")

@app.get("/css/responsive.css", tags=["Frontend"])
async def get_responsive_css():
    return Response(content=RESPONSIVE_CSS, media_type="text/css")

@app.get("/js/main.js", tags=["Frontend"])
async def get_main_js():
    return Response(content=MAIN_JS, media_type="application/javascript")

@app.get("/js/form.js", tags=["Frontend"])
async def get_form_js():
    return Response(content=FORM_JS, media_type="application/javascript")

# ==========================================
# 11. APPLICATION ENTRYPOINT
# ==========================================
if __name__ == "__main__":
    print("Starting FastForge Startup Website Single-File Server...")
    print("Access your website at: http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
