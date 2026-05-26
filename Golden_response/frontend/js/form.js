const form = document.getElementById("contact-form");
const message = document.getElementById("form-message");

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
        const isLocal = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1" || !window.location.hostname;
        const apiUrl = isLocal ? "http://127.0.0.1:8000/api/contact" : "/api/contact";

        const response = await fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });

        const result = await response.json();

        if (response.ok) {
            message.innerText = result.message;
            form.reset();
        } else {
            message.innerText = result.message;
        }
    } catch (error) {
        message.innerText = "Server error";
    }
});
