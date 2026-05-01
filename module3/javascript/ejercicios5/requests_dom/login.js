// login.js — Login page logic
// This runs when the user opens login.html.
// It reads the User ID and password, validates them,
// then calls loginUser() from db.js to check the credentials.

// If already logged in, go straight to profile
if (isLoggedIn()) {
  window.location.href = 'profile.html';
}

// Grab the elements from the HTML
var form = document.getElementById('loginForm');
var alertBox = document.getElementById('alert');
var submitBtn = document.getElementById('submitBtn');
var userIdInput = document.getElementById('userId');
var rememberCheckbox = document.getElementById('rememberMe');

// The key we use to store the remembered User ID
var REMEMBER_KEY = 'lyfter_remember_id';

// If the user checked "Remember Me" last time, pre-fill their ID
var savedId = localStorage.getItem(REMEMBER_KEY);
if (savedId !== null) {
  userIdInput.value = savedId;
  rememberCheckbox.checked = true;
}

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
  event.preventDefault();
  hideAlert();

  // Read the input values
  var userId = userIdInput.value.trim();
  var password = document.getElementById('password').value;

  // ── Basic validation ──────────────────────────────────────────────────────

  if (userId === '') {
    showAlert('Please enter your User ID.', 'error');
    return;
  }

  if (password === '') {
    showAlert('Please enter your password.', 'error');
    return;
  }

  // ── Disable button while waiting for the fake API response ───────────────
  submitBtn.disabled = true;
  submitBtn.textContent = 'Logging in...';

  // ── Call loginUser() and handle the result ────────────────────────────────
  loginUser(userId, password)
    .then(function(user) {
      // Save or remove the remembered ID based on the checkbox
      if (rememberCheckbox.checked) {
        localStorage.setItem(REMEMBER_KEY, userId);
      } else {
        localStorage.removeItem(REMEMBER_KEY);
      }

      // Save the session and go to profile
      saveSession(user);
      window.location.href = 'profile.html';
    })
    .catch(function(error) {
      // Show the error (e.g. "User not found" or "Incorrect password")
      showAlert(error.message, 'error');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Log In';
    });
});
