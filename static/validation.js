const form = document.getElementById("login-form");
const email_input = document.getElementById("email-input");
const password_input = document.getElementById("password-input");
const confirm_password_input = document.getElementById("confirm-password-input");
const error_message = document.getElementById('error-message')

form.addEventListener('submit', (ev) => {
    // ev.preventDefault();

    let errors = [];

    errors = getSignupFormErrors(email_input.value, password_input.value, confirm_password_input.value);

    // Prevent form submission when errors are present
    if (errors.length > 0) {
        ev.preventDefault();
        error_message.innerText = errors.join(". ");
    }

    // TODO: Create if-else statement with login form errors after login page 
    // is created
});

function getSignupFormErrors(email, password, confirmPassword) {
    let errors = []

    // TODO: add "incorrect" to class lists after incorrect is implemented in HTML/CSS

    // Empty inputs
    if (email === '' || email === null) {
        errors.push("Email is required");
    }

    if (password === '' || password === null) {
        errors.push("Password is required");
    }

    if (confirmPassword !== password) {
        errors.push("Passwords do not match");
    }

    return errors;
}
