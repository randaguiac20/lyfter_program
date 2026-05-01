// change-password.js — Change Password page logic
// This runs when the user opens change-password.html.
// It can be used by a logged-in user (whose ID is pre-filled)
// OR by any visitor who knows their User ID.

// Get the current session (may be null if not logged in)
var currentUser = getSession();

// Get the elements from the HTML
var form = document.getElementById('changePasswordForm');
var alertBox = document.getElementById('alert');
var submitBtn = document.getElementById('submitBtn');
var navLinks = document.getElementById('navLinks');

// ── Set up the navigation bar based on login state ────────────────────────

if (currentUser !== null) {
  // User is logged in: pre-fill the User ID and show a logout button
  document.getElementById('userId').value = currentUser.id;

  navLinks.innerHTML =
    '<a href="profile.html">My Profile</a>' +
    '<button id="navLogoutBtn">Log Out</button>';

  document.getElementById('navLogoutBtn').addEventListener('click', function() {
    clearSession();
    window.location.href = 'login.html';
  });
} else {
  // User is NOT logged in: show register and login links
  navLinks.innerHTML =
    '<a href="register.html">Register</a>' +
    '<a href="login.html">Login</a>';
}

// ── Helper functions ──────────────────────────────────────────────────────

function showAlert(message, type) {
  alertBox.textContent = message;
  alertBox.className = 'alert alert-' + type;
}

function hideAlert() {
  alertBox.textContent = '';
  alertBox.className = 'alert hidden';
}

// ── Form submission ───────────────────────────────────────────────────────

form.addEventListener('submit', function(event) {
  event.preventDefault();
  hideAlert();

  // Read the input fields
  var userId = document.getElementById('userId').value.trim();
  var oldPassword = document.getElementById('oldPassword').value;
  var newPassword = document.getElementById('newPassword').value;
  var confirmPassword = document.getElementById('confirmPassword').value;

  // ── Basic validation ──────────────────────────────────────────────────────

  if (userId === '') {
    showAlert('Please enter your User ID.', 'error');
    return;
  }

  if (oldPassword === '') {
    showAlert('Please enter your current password.', 'error');
    return;
  }

  if (newPassword === '') {
    showAlert('Please enter a new password.', 'error');
    return;
  }

  if (newPassword.length < 6) {
    showAlert('New password must be at least 6 characters long.', 'error');
    return;
  }

  if (confirmPassword === '') {
    showAlert('Please confirm your new password.', 'error');
    return;
  }

  if (newPassword !== confirmPassword) {
    showAlert('New passwords do not match.', 'error');
    return;
  }

  // ── Disable button while waiting ──────────────────────────────────────────
  submitBtn.disabled = true;
  submitBtn.textContent = 'Updating...';

  // ── Call changePassword() from db.js ──────────────────────────────────────
  changePassword(userId, oldPassword, newPassword)
    .then(function() {
      showAlert('Password updated successfully!', 'success');
      form.reset();

      // If the logged-in user just changed their own password,
      // log them out so they sign in again with the new password
      if (currentUser !== null && currentUser.id === userId) {
        showAlert('Password updated! Redirecting to login...', 'success');
        clearSession();
        setTimeout(function() {
          window.location.href = 'login.html';
        }, 2000);
      } else {
        // Not the current user — re-enable the form
        if (currentUser !== null) {
          document.getElementById('userId').value = currentUser.id;
        }
        submitBtn.disabled = false;
        submitBtn.textContent = 'Update Password';
      }
    })
    .catch(function(error) {
      // Show error (e.g. "User not found" or "Current password is incorrect")
      showAlert(error.message, 'error');
      submitBtn.disabled = false;
      submitBtn.textContent = 'Update Password';
    });
});
