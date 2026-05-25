Prompt

Context and Role

So basically I am a developer who knows Python well and I want to build my own business website. For backend I will use FastAPI and for frontend simple HTML, CSS, JavaScript — no React or anything. The site should look clean and professional like a proper startup website, load fast, and everything should work properly on mobile also.

Objective

I want to build a complete website where:

Frontend is made with HTML, CSS, vanilla JS — simple but good looking  
All dynamic stuff like form submission, data fetching — handled by FastAPI backend  
Contact form should work properly — save data in DB and send me an email  
Website should come good on Google search also  
Code should be clean, folders properly organized, easy to understand  
At the end it should run on Docker so I can deploy it on any server

UI and Layout Requirements

Page Sections  
My website will have these sections — all on one page or separate pages, whatever looks better:			  
Hero Section — big heading, one line about my business, a button like "Get Started" or "Book a Demo"  
About Section — short intro about my company, what we do, our mission  
Services / Features Section — show my services in cards or grid layout  
How It Works Section — explain my process step by step with icons or numbers  
Testimonials Section — what my clients say, with their name and designation  
Pricing Section (optional) — show my plans, highlight the recommended one  
FAQ Section — common questions in accordion style, click to open and close  
Contact Section — form where people message me, plus my phone and email shown below  
Footer — logo, nav links, social media icons, copyright line

Design Requirements

Should look good on mobile, tablet and desktop — fully responsive  
Use CSS variables for colors, fonts, spacing so everything stays consistent  
Smooth scroll when user clicks on nav links  
Hamburger menu on mobile  
Nice hover effects on buttons, cards and links  
Good font from Google Fonts  
Proper HTML5 tags, ARIA labels so accessibility is also fine

Frontend Functionality 

Navbar should stick on top and change style a little when user scrolls down  
Clicking nav links should smoothly scroll to that section  
Hamburger menu should open and close on mobile  
FAQ accordion — click question, answer opens, click again it closes  
Contact form should check all fields before sending — show error if something is wrong  
Use Fetch API to send form data to FastAPI backend, no page reload  
After form submit show success or error message to user on same page  
Images should load lazily — don't load everything at once  
Sections should fade in nicely when user scrolls to them — use Intersection Observer for that

Backend Requirements (FastAPI)  
API Endpoints

POST /api/contact — take form data, validate it, save in DB, send me email  
GET /api/health — just check if server is running fine  
GET /api/testimonials — return testimonials list from DB or JSON file  
GET /api/services — return my services list dynamically  
POST /api/newsletter — save user email for newsletter

Request / Response Schema  
Every API should return proper JSON only:

Success: { status: "success", message: "...", data: {...}, timestamp }  
Error: { status: "error", error\_code: "...", message: "...", details: {...} }

Contact Form Fields

Full Name (required)  
Business Email (required, proper email format check)  
Phone Number (required, validated)  
Company Name (optional)  
Service of Interest (dropdown, optional)  
Message (required)

Validation and Security

Use Pydantic v2 to validate all form data coming in  
Clean all inputs properly — no XSS, no injection attacks  
Add rate limiting on contact and newsletter API so nobody spams it  
CORS should only allow my frontend origin, not everyone  
All passwords, keys, credentials — only in environment variables, never written directly in code  
Add simple spam protection — honeypot field or basic CAPTCHA

Email Notification System

When someone submits the contact form, I should get an email on my id with:

Their Full Name  
Email  
Phone Number  
Company Name  
Which service they are interested in  
Their Message  
Time when they submitted

Use aiosmtplib for sending email async way so server doesn't slow down  
Also send a confirmation email to the user saying "we received your message"  
If email fails for some reason — log it, don't crash, try again if possible, still show success to user

Data Storage Requirements

Save all contact form submissions in a database — PostgreSQL for production, SQLite for testing locally  
Use SQLAlchemy with async support  
Contact table should have: id, name, email, phone, company, service, message, created\_at  
Newsletter emails go in a separate table  
Use Alembic for database migrations — proper way, no manual table creation

Configuration Management

All settings go in a .env file — nothing hardcoded  
Use python-dotenv to load them  
These env variables are must:

DATABASE\_URL  
SMTP\_HOST, SMTP\_PORT, SMTP\_USER, SMTP\_PASSWORD  
OWNER\_EMAIL  
ALLOWED\_ORIGINS  
SECRET\_API\_KEY  
ENVIRONMENT (development / staging / production)

When server starts, check all required variables are present — if something missing, show clear error and stop

Logging and Monitoring

Use Python logging properly — structured format  
Every API request should be logged — method, path, status, how long it took  
Log every form submission — but don't log sensitive stuff like passwords  
Log every email send — success or failure both  
If any unhandled error comes — log full stack trace  
Separate log files: app.log, errors.log, submissions.log

Technology Stack

Frontend

HTML5 — proper semantic tags  
CSS3 — Flexbox, Grid, variables, animations  
Vanilla JavaScript ES6+ — Fetch API, DOM, Intersection Observer  
Google Fonts — for good typography  
Font Awesome or Heroicons — for icons

Backend

Python 3.11+  
FastAPI — main backend framework  
Pydantic v2 — validation  
Uvicorn — to run the server  
SQLAlchemy async — ORM for database  
Alembic — migrations  
aiosmtplib — async email  
slowapi — rate limiting  
python-dotenv — env variables

Database

PostgreSQL — for production  
SQLite — for local development and testing

Testing & Quality

pytest \+ httpx — to test all APIs  
ruff / black — code formatting and linting  
pre-commit hooks — so bad code doesn't go in git

Infrastructure

Docker \+ docker-compose — run everything in containers  
Nginx — serve frontend files and forward API requests to FastAPI

Error Handling and Documentation

Make custom exception classes — ValidationError, EmailSendError, DatabaseError  
FastAPI global exception handler — so every error returns same format response  
In production never show internal error details to user — keep it safe  
FastAPI auto docs at /docs and /redoc — use them, don't make separate docs manually  
Write a proper README.md with:

What this project is  
Folder structure  
How to run locally  
All env variables explained  
How to run with Docker  
How to deploy

Output Requirements

Full website working in browser — all sections looking good  
Frontend talking to backend properly — all API calls working  
Contact form saves in DB and I get email on submission  
User sees success message after submitting form  
Health check API working  
API docs accessible at /docs  
If 404 or 500 error comes — show a proper styled error page, not ugly default one

Performance and SEO

Minify CSS and JS before going to production  
Use WebP images, compress everything  
Add proper meta tags — title, description, Open Graph, Twitter Card  
Semantic HTML so Google can read it properly  
Lighthouse score should be 90+ on desktop  
Add robots.txt and sitemap.xml  
Use defer or async on script tags — don't block page load

Suggested Folder Structure  
startup\_website/  
  frontend/  
    index.html  
    about.html  
    css/  
      style.css  
      responsive.css  
      animations.css  
    js/  
      main.js  
      form.js  
      nav.js  
    assets/  
      images/  
      icons/  
  backend/  
    app/  
      main.py  
      routes/       contact.py, newsletter.py, health.py  
      models/       submission.py, subscriber.py  
      schemas/      contact.py, newsletter.py  
      services/     email.py, database.py  
      utils/        logger.py, validators.py, exceptions.py  
    migrations/  
    tests/  
    .env.example  
    requirements.txt  
    Dockerfile  
  docker-compose.yml  
  nginx.conf  
  README.md

