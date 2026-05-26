# Full-Stack Business Startup Website (FastAPI + Vanilla JS)

## Project Overview

So basically I am a developer who knows Python well and I want to build my own business website. For backend I will use FastAPI and for frontend simple HTML, CSS, JavaScript — no React or anything. The site should look clean and professional like a proper startup website, load fast, and everything should work properly on mobile also.

The project should include:

1 Clean professional UI with smooth animations
2 FastAPI backend with proper REST APIs
4 Contact form that saves data in DB and sends me email
5 SEO-friendly so it comes good on Google search
6 Everything runs on Docker so I can deploy it on any server

---

# Tech Stack

- HTML5 - proper semantic tags
- CSS3 - Flexbox, Grid, variables, animations
- Vanilla JavaScript ES6+ - Fetch API, Intersection Observer, DOM
- Google Fonts - for good typography
- Font Awesome or Heroicons - for icons
- Python 3.11+ with FastAPI
- Pydantic v2 - validation
- Uvicorn - to run the server
- SQLAlchemy async - ORM for database
- Alembic - migrations
- PostgreSQL (production) / SQLite (local dev)
- aiosmtplib - async email
- slowapi - rate limiting
- python-dotenv - env variables
- Docker + docker-compose + Nginx

---

# Project Structure

```bash
startup_website/
│
├── frontend/               → All frontend files
│   ├── index.html
│   ├── about.html
│   ├── css/
│   │   ├── style.css
│   │   ├── responsive.css
│   │   └── animations.css
│   ├── js/
│   │   ├── main.js
│   │   ├── form.js
│   │   └── nav.js
│   └── assets/
│       ├── images/
│       └── icons/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/         → contact.py, newsletter.py, health.py
│   │   ├── models/         → submission.py, subscriber.py
│   │   ├── schemas/        → contact.py, newsletter.py
│   │   ├── services/       → email.py, database.py
│   │   └── utils/          → logger.py, validators.py, exceptions.py
│   ├── migrations/
│   ├── tests/
│   ├── .env.example
│   ├── requirements.txt
│   └── Dockerfile
│
├── docker-compose.yml
├── nginx.conf
└── README.md
```

---

# FEATURES REQUIRED

## 1. PAGE SECTIONS

My website will have these sections — all on one page or separate pages, whatever looks better:

- **Hero Section** - big heading, one line about my business, a button like "Get Started" or "Book a Demo"
- **About Section** - short intro about my company, what we do, our mission
- **Services / Features Section** - show my services in cards or grid layout
- **How It Works Section** - explain my process step by step with icons or numbers
- **Testimonials Section** - what my clients say, with their name and designation
- **Pricing Section** *(optional)* - show my plans, highlight the recommended one
- **FAQ Section** - common questions in accordion style, click to open and close
- **Contact Section** - form where people message me, plus my phone and email shown below
- **Footer** - logo, nav links, social media icons, copyright line

---

## 2. DESIGN REQUIREMENTS

Should look good on mobile, tablet and desktop — fully responsive:

- Use CSS variables for colors, fonts, spacing so everything stays consistent
- Smooth scroll when user clicks on nav links
- Hamburger menu on mobile
- Nice hover effects on buttons, cards and links
- Good font from Google Fonts
- Proper HTML5 tags, ARIA labels so accessibility is also fine

---

## 3. FRONTEND FUNCTIONALITY

- Navbar should stick on top and change style a little when user scrolls down
- Clicking nav links should smoothly scroll to that section
- Hamburger menu should open and close on mobile
- FAQ accordion - click question, answer opens, click again it closes
- Contact form should check all fields before sending — show error if something is wrong
- Use Fetch API to send form data to FastAPI backend, no page reload
- After form submit show success or error message to user on same page
- Images should load lazily - don't load everything at once
- Sections should fade in nicely when user scrolls to them - use Intersection Observer for that

---

## 4. BACKEND API ENDPOINTS

```
POST /api/contact       → Take form data, validate it, save in DB, send me email
GET  /api/health        → Just check if server is running fine
GET  /api/testimonials  → Return testimonials list from DB or JSON file
GET  /api/services      → Return my services list dynamically
POST /api/newsletter    → Save user email for newsletter
```

---

## 5. REQUEST / RESPONSE FORMAT

Every API should return proper JSON only:

**Success:**
```json
{
  "status": "success",
  "message": "...",
  "data": {},
  "timestamp": "..."
}
```

**Error:**
```json
{
  "status": "error",
  "error_code": "...",
  "message": "...",
  "details": {}
}
```

---

## 6. CONTACT FORM FIELDS

- Full Name *(required)*
- Business Email *(required, proper email format check)*
- Phone Number *(required, validated)*
- Company Name *(optional)*
- Service of Interest *(dropdown, optional)*
- Message *(required)*

---

## 7. VALIDATION AND SECURITY

- Use Pydantic v2 to validate all form data coming in
- Clean all inputs properly - no XSS, no injection attacks
- Add rate limiting on contact and newsletter API so nobody spams it
- CORS should only allow my frontend origin, not everyone
- All passwords, keys, credentials - only in environment variables, never written directly in code
- Add simple spam protection — honeypot field or basic CAPTCHA

---

## 8. EMAIL NOTIFICATION SYSTEM

When someone submits the contact form, I should get an email on my id with:

- Their Full Name
- Email
- Phone Number
- Company Name
- Which service they are interested in
- Their Message
- Time when they submitted

Also send a confirmation email to the user saying "we received your message".

Additional behavior:
- Use aiosmtplib for sending email async way so server doesn't slow down
- If email fails for some reason — log it, don't crash, try again if possible, still show success to user

---

## 9. DATA STORAGE

- Save all contact form submissions in a database — PostgreSQL for production, SQLite for testing locally
- Use SQLAlchemy with async support
- Contact table should have: `id`, `name`, `email`, `phone`, `company`, `service`, `message`, `created_at`
- Newsletter emails go in a separate table
- Use Alembic for database migrations — proper way, no manual table creation

---

## 10. ENVIRONMENT VARIABLES

All settings go in a `.env` file — nothing hardcoded:

```env
DATABASE_URL
SMTP_HOST
SMTP_PORT
SMTP_USER
SMTP_PASSWORD
OWNER_EMAIL
ALLOWED_ORIGINS
SECRET_API_KEY
ENVIRONMENT       # development / staging / production
```

When server starts, check all required variables are present — if something missing, show clear error and stop.

---

## 11. LOGGING AND MONITORING

- Use Python logging properly - structured format
- Every API request should be logged - method, path, status, how long it took
- Log every form submission - but don't log sensitive stuff like passwords
- Log every email send - success or failure both
- If any unhandled error comes - log full stack trace
- Separate log files: `app.log`, `errors.log`, `submissions.log`

---

## 12. TESTING AND CODE QUALITY

- pytest + httpx - to test all APIs
- ruff / black - code formatting and linting
- pre-commit hooks - so bad code doesn't go in git

---

## 13. ERROR HANDLING

- Make custom exception classes - `ValidationError`, `EmailSendError`, `DatabaseError`
- FastAPI global exception handler - so every error returns same format response
- In production never show internal error details to user - keep it safe
- If 404 or 500 error comes - show a proper styled error page, not ugly default one

---

## 14. INFRASTRUCTURE

- Docker + docker-compose - run everything in containers
- Nginx - serve frontend files and forward API requests to FastAPI
- Minify CSS and JS before going to production
- Use WebP images, compress everything

---

## 15. SEO AND PERFORMANCE

- Add proper meta tags - title, description, Open Graph, Twitter Card
- Semantic HTML so Google can read it properly
- Lighthouse score should be 90+ on desktop
- Add robots.txt and sitemap.xml
- Use defer or async on script tags - don't block page load

---

## 16. API DOCUMENTATION

- FastAPI auto docs at `/docs` and `/redoc` - use them, don't make separate docs manually
- Write a proper README.md with:
  - What this project is
  - Folder structure
  - How to run locally
  - All env variables explained
  - How to run with Docker
  - How to deploy

---

## 17. FINAL OUTPUT REQUIRED

Provide:

- Full website working in browser - all sections looking good
- Frontend talking to backend properly - all API calls working
- Contact form saves in DB and I get email on submission
- User sees success message after submitting form
- Health check API working
- API docs accessible at `/docs`
- Proper styled 404 and 500 error pages

---

# DEVELOPMENT FLOW

Build the project step-by-step starting from:

1. Project folder structure setup
2. Backend - FastAPI app, config, env loading
3. Database - SQLAlchemy models, Alembic migrations
4. Backend routes - contact, newsletter, health APIs
5. Email service - async sending with aiosmtplib
6. Logging setup - app, errors, submissions log files
7. Frontend - HTML structure, all sections
8. Frontend - CSS styling, responsive layout, animations
9. Frontend - JavaScript for nav, FAQ, form, scroll effects
10. Integration - connect frontend to backend APIs
11. Docker + Nginx configuration
12. Testing - pytest for all API endpoints
13. Final polish - SEO tags, performance, README

---

# FINAL GOAL

The final project should work as a complete production-ready business website where everything is properly connected - frontend to backend, form saves to DB, I get email notifications, and the whole thing runs on Docker so I can deploy it on any server easily.
