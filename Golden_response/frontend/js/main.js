// Intersection Observer for fade-in animations
const observer = new IntersectionObserver((entries) => {
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

// Hamburger menu toggle
const hamburger = document.getElementById("hamburger");
const navLinks = document.getElementById("nav-links");

if (hamburger && navLinks) {
    hamburger.addEventListener("click", () => {
        navLinks.classList.toggle("active");
    });
}

// Dynamic loading of Services and Testimonials
document.addEventListener("DOMContentLoaded", () => {
    loadServices();
    loadTestimonials();
});

const isLocal = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || !window.location.hostname;
const backendUrl = isLocal ? "http://127.0.0.1:8000" : "";

async function loadServices() {
    const grid = document.getElementById("services-grid");
    if (!grid) return;

    try {
        const response = await fetch(`${backendUrl}/api/services`);
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
        const response = await fetch(`${backendUrl}/api/testimonials`);
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
