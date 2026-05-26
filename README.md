# FastForge

### Production-Ready Startup Website — FastAPI + Vanilla JS

---

## What Is This?

So basically I am a Python developer and I wanted to build my own business website — but without React, Next.js, or any heavy frontend framework. Just clean HTML, CSS, and vanilla JavaScript on the frontend, and FastAPI doing all the backend work.

**FastForge** is that website — but built properly. Not just a quick template, but a full production-ready setup that you can actually deploy on any server, configure with environment variables, and trust in production. Contact form saves to a real database, sends you email notifications, has rate limiting so nobody spams it, and everything runs inside Docker so deployment is just one command.

If you are a solo developer who knows Python and wants a professional business website without the JavaScript framework headache — this is exactly what you need.

---

## Key Features

| Feature | Details |
|---|---|
| **Lightning Fast** | No framework overhead — pure HTML/CSS/JS frontend |
| **Secure by Default** | Rate limiting, input sanitization, honeypot spam protection |
| **Fully Responsive** | Works on mobile, tablet, and desktop — properly |
| **Docker Ready** | One command and everything is running |
| **Async Email** | Contact form sends you email instantly using aiosmtplib |
| **Real Database** | PostgreSQL in production, SQLite for local testing |
| **Pydantic v2 Validation** | All form data validated properly before anything is saved |
| **Auto API Docs** | FastAPI generates `/docs` and `/redoc` automatically |
| **SEO Ready** | Meta tags, Open Graph, robots.txt, sitemap.xml all included |
| **Proper Logging** | Separate log files for app, errors, and form submissions |

---

## Tech Stack

### Backend
- **FastAPI** — main backend framework, async and fast
- **Uvicorn** — ASGI server to run FastAPI
- **SQLAlchemy (async)** — ORM for database operations
- **AsyncPG** — ultra-fast PostgreSQL driver
- **Pydantic v2** — data validation and schema management
- **Alembic** — database migrations, proper way
- **Slowapi** — rate limiting on APIs
- **Aiosmtplib** — sending emails the async way
- **Python-dotenv** — loading environment variables from `.env`

### Frontend
- **HTML5** — semantic tags, ARIA labels for accessibility
- **CSS3** — variables, Flexbox, Grid, animations
- **Vanilla JavaScript ES6+** — Fetch API, Intersection Observer, DOM
- **Google Fonts** — good typography
- **Font Awesome / Heroicons** — icons

### Database
- **PostgreSQL** — for production
- **SQLite** — for local development and testing

### Infrastructure
- **Docker + Docker Compose** — containerized everything
- **Nginx** — serves frontend files, forwards API calls to FastAPI

---

## Folder Structure

```
FastForge/
│
├── frontend/
│   ├── index.html                  # Main page — all sections here
│   ├── robots.txt                  # SEO — tells Google what to crawl
│   ├── sitemap.xml                 # Sitemap for search engines
│   │
│   ├── css/
│   │   ├── style.css               # Core styles, colors, typography
│   │   └── responsive.css          # Mobile and tablet breakpoints
│   │
│   ├── js/
│   │   ├── main.js                 # Navbar, FAQ accordion, scroll effects
│   │   └── form.js                 # Contact form — validation + API call
│   │
│   └── assets/
│       ├── images/                 # WebP images, compressed
│       └── icons/                  # SVG icons
│
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI app setup, middleware, CORS
│   │   ├── config.py               # All env variables loaded here
│   │   ├── database.py             # DB connection, async session setup
│   │   │
│   │   ├── routes/
│   │   │   ├── contact.py          # POST /api/contact
│   │   │   └── health.py           # GET /api/health
│   │   │
│   │   ├── models/
│   │   │   └── contact.py          # SQLAlchemy table models
│   │   │
│   │   ├── schemas/
│   │   │   └── contact.py          # Pydantic request/response schemas
│   │   │
│   │   └── services/
│   │       └── email_service.py    # Async email sending logic
│   │
│   ├── migrations/                 # Alembic migration files
│   ├── tests/                      # pytest test files
│   ├── requirements.txt            # All Python dependencies
│   ├── .env.example                # Template — copy this to .env
│   └── Dockerfile                  # Backend container definition
│
├── docker-compose.yml              # Runs frontend + backend + DB together
├── nginx.conf                      # Nginx config — proxy + static files
├── run_locally.bat                 # Windows — run project with one click
├── run_locally.ps1                 # PowerShell alternative
├── .gitignore
└── README.md
```

---

## Environment Variables

Copy `.env.example` to `.env` inside the `backend/` folder and fill in your values.

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost/fastforge

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASSWORD=your_app_password

# Who gets the contact form emails
OWNER_EMAIL=your@email.com

# Security
ALLOWED_ORIGINS=http://localhost:5500
SECRET_API_KEY=your_secret_key_here

# Environment
ENVIRONMENT=development    # development / staging / production
```

> Note: When the server starts, it checks all required variables are present. If something is missing, it shows a clear error and stops — it won't start with broken config.

---

## Running Locally (Without Docker)

### Option 1 — One Command (Windows)

Just run this from the root folder:

```bat
.\run_locally.bat
```

This starts both backend and frontend together automatically.

---

### Option 2 — Run Separately

**Step 1 — Start the Backend**

```powershell
cd backend
py -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Step 2 — Start the Frontend**

```powershell
cd frontend
py -m http.server 5500
```

Then open your browser and go to:

- Website → `http://127.0.0.1:5500`
- API Docs → `http://127.0.0.1:8000/docs`
- Redoc → `http://127.0.0.1:8000/redoc`

---

## Running with Docker

Make sure Docker Desktop is running, then from the root folder:

```bash
docker-compose up --build
```

This starts everything — PostgreSQL database, FastAPI backend, and Nginx serving the frontend.

- Website → `http://localhost`
- API Docs → `http://localhost/docs`

To stop everything:

```bash
docker-compose down
```

To stop and also delete the database volume:

```bash
docker-compose down -v
```

---

## Database Setup

Migrations are handled by Alembic — no manual table creation needed.

**Run migrations:**

```bash
cd backend
alembic upgrade head
```

**Create a new migration after model changes:**

```bash
alembic revision --autogenerate -m "your migration message"
```

---

## API Endpoints

| Method | Endpoint | What It Does |
|---|---|---|
| `POST` | `/api/contact` | Takes form data, validates, saves to DB, sends email |
| `GET` | `/api/health` | Quick check — is the server running fine? |
| `GET` | `/api/testimonials` | Returns testimonials list |
| `GET` | `/api/services` | Returns services list dynamically |
| `POST` | `/api/newsletter` | Saves email for newsletter |

### Response Format

Every API returns the same clean JSON structure:

**Success:**
```json
{
  "status": "success",
  "message": "Your message has been received.",
  "data": {},
  "timestamp": "2024-01-15T10:30:00Z"
}
```

**Error:**
```json
{
  "status": "error",
  "error_code": "VALIDATION_ERROR",
  "message": "Please check the fields and try again.",
  "details": {}
}
```

---

## Contact Form Fields

When someone fills the contact form, these fields are collected and validated:

| Field | Type | Required |
|---|---|---|
| Full Name | Text | Yes |
| Business Email | Email (validated format) | Yes |
| Phone Number | Phone (validated) | Yes |
| Company Name | Text | Optional |
| Service of Interest | Dropdown | Optional |
| Message | Textarea | Yes |

---

## Email Notifications

When someone submits the contact form:

1. **You get an email** with their full details — name, email, phone, company, service interest, message, and submission time
2. **They get a confirmation email** saying their message was received

Email sending is async — the server doesn't wait for it, so form submission feels instant. If email fails for any reason — it logs the error, doesn't crash the server, and still shows success to the user.

---

## Logging

Three separate log files are maintained:

| Log File | What Gets Logged |
|---|---|
| `app.log` | Every API request — method, path, status, response time |
| `errors.log` | Full stack traces for any unhandled errors |
| `submissions.log` | Every form submission — without sensitive data |

---

## Security

- **Rate limiting** — contact and newsletter APIs are rate limited so nobody can spam them
- **Input sanitization** — all form data is cleaned, no XSS or injection attacks possible
- **Honeypot field** — basic spam protection built into the contact form
- **CORS** — only your frontend origin is allowed, not open to everyone
- **Environment variables** — all credentials and keys in `.env` only, never hardcoded
- **Pydantic v2** — strict validation on all incoming data before anything is processed

---

## Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## Installing Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

## SEO and Performance

- Meta tags for title, description, Open Graph, Twitter Card — all set
- `robots.txt` and `sitemap.xml` included
- Semantic HTML so Google can read the page properly
- Script tags use `defer` — don't block page load
- Images are WebP format and compressed
- Target Lighthouse score 90+ on desktop

---

## License

This project is open source. Use it, modify it, deploy it — it's yours.

---

## Built By

Made by a solo Python developer who just wanted a clean business website without the JavaScript framework drama.

> If this helped you — star the repo, share it, or just build something cool with it.
