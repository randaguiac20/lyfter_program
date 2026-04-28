// register.js — Registration page logic
// This runs when the user opens register.html.
// It reads the form fields, validates them, then calls createUser()
// from db.js to save the new user.

// If the user is already logged in, send them straight to the profile page
if (isLoggedIn()) {
  window.location.href = 'profile.html';
}

// Grab the form and the alert box from the HTML
var form = document.getElementById('registerForm');
var alertBox = document.getElementById('alert');
var submitButton = document.getElementById('submitButton');

// Helper: show a message at the top of the card
function showAlert(message, type) {
  alertBox.textContent = message;
  alertBox.className = 'alert alert-' + type;
}

// Helper: hide the alert box
function hideAlert() {
  alertBox.textContent = '';
  alertBox.className = 'alert hidden';
}

// When the form is submitted...
form.addEventListener('submit', function(event) {
  // Stop the page from reloading (default browser behavior)
  event.preventDefault();
  hideAlert();

  // Read each input field
  var name = document.getElementById('name').value.trim();
  var email = document.getElementById('email').value.trim();
  var phone = document.getElementById('phone').value.trim();
  var age = document.getElementById('age').value;
  var password = document.getElementById('password').value;
  var confirmPassword = document.getElementById('confirmPassword').value;

  // ── Validation: check each field one by one ──────────────────────────────

  if (name === '') {
    showAlert('Please enter your full name.', 'error');
    return;
  }

  if (email === '') {
    showAlert('Please enter your email.', 'error');
    return;
  }

  // Simple email check: must have @ and a dot after it
  if (email.indexOf('@') === -1 || email.indexOf('.') === -1) {
    showAlert('Please enter a valid email address.', 'error');
    return;
  }

  if (phone === '') {
    showAlert('Please enter your phone number.', 'error');
    return;
  }

  if (age === '') {
    showAlert('Please enter your age.', 'error');
    return;
  }

  var ageNumber = parseInt(age);
  if (ageNumber < 1 || ageNumber > 120) {
    showAlert('Please enter a valid age between 1 and 120.', 'error');
    return;
  }

  if (password === '') {
    showAlert('Please enter a password.', 'error');
    return;
  }

  if (password.length < 6) {
    showAlert('Password must be at least 6 characters long.', 'error');
    return;
  }

  if (confirmPassword === '') {
    showAlert('Please confirm your password.', 'error');
    return;
  }

  if (password !== confirmPassword) {
    showAlert('Passwords do not match.', 'error');
    return;
  }

  // ── Build the user object to send to the fake API ────────────────────────
  // This shape matches what createUser() expects
  var newUser = {
    name: name,
    password: password,
    data: {
      email: email,
      phone: phone,
      age: ageNumber
    }
  };

  // ── Disable the button so the user can't click twice ─────────────────────
  submitButton.disabled = true;
  submitButton.textContent = 'Creating account...';

  // ── Call createUser() and handle the result ───────────────────────────────
  // .then() runs if everything goes well
  // .catch() runs if there is an error (e.g. email already taken)
  createUser(newUser)
    .then(function(createdUser) {
      // Save the session so we know who is logged in
      saveSession(createdUser);

      // Tell the user their new ID — they need it to log in later
      alert(
        'Account created successfully!\n\n' +
        'Your User ID is:\n' +
        createdUser.id + '\n\n' +
        'Please save this — you will need it to log in.'
      );

      // Go to the profile page
      window.location.href = 'profile.html';
    })
    .catch(function(error) {
      // Something went wrong — show the error and re-enable the button
      showAlert(error.message, 'error');
      submitButton.disabled = false;
      submitButton.textContent = 'Create Account';
    });
});
