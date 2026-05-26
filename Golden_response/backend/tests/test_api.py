import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app

@pytest.mark.anyio
async def test_health_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "API healthy"

@pytest.mark.anyio
async def test_services_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/services")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) > 0

@pytest.mark.anyio
async def test_testimonials_endpoint():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/testimonials")
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert len(response.json()["data"]) > 0

@pytest.mark.anyio
async def test_newsletter_endpoint():
    import time
    email = f"user_{int(time.time())}@example.com"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/newsletter", json={"email": email})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "subscribed" in response.json()["message"]

@pytest.mark.anyio
async def test_contact_endpoint():
    payload = {
        "full_name": "Test User",
        "business_email": "test@example.com",
        "phone_number": "1234567890",
        "message": "This is a test message to verify the contact endpoint."
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/contact", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
