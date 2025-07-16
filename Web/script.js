document.addEventListener("DOMContentLoaded", function() {
    const registrationForm = document.getElementById("registrationForm");
    const loginForm = document.getElementById("loginForm");

    registrationForm.addEventListener("submit", function(event) {
        event.preventDefault();
        // Handle user registration logic here
        alert("User registered!");
    });

    loginForm.addEventListener("submit", function(event) {
        event.preventDefault();

        // Assume successful login for demonstration
        // In a real-world scenario, you should validate the user's credentials on the server
        const userEmail = document.getElementById("loginEmail").value;

        // Redirect to booking page after successful login
        window.location.href = `booking.html?user=${userEmail}`;
    });
});