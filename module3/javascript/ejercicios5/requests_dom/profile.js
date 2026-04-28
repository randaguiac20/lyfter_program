// profile.js — Profile page logic
// This runs when the user opens profile.html.
// It reads the current session, then builds the profile card HTML
// and injects it into the page.

// If not logged in, send the user to the login page
if (!isLoggedIn()) {
  window.location.href = 'login.html';
}

// Get the current logged-in user from session
var user = getSession();

// Get the profile card element from the HTML
var profileCard = document.getElementById('profileCard');

// Helper: get the first two initials from a name (e.g. "John Doe" → "JD")
function getInitials(name) {
  var words = name.split(' ');
  var initials = '';
  if (words[0]) {
    initials = initials + words[0][0];
  }
  if (words[1]) {
    initials = initials + words[1][0];
  }
  return initials.toUpperCase();
}

// Helper: format a date string into something readable (e.g. "April 28, 2026")
function formatDate(isoString) {
  if (!isoString) {
    return 'N/A';
  }
  var date = new Date(isoString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
}

// Helper: log the user out
function logout() {
  clearSession();
  window.location.href = 'login.html';
}

// Build the profile card HTML using string concatenation
// We read user.data for the extra info (email, phone, age)
var data = user.data;

profileCard.innerHTML =
  '<div class="profile-header">' +
    '<div class="avatar">' + getInitials(user.name) + '</div>' +
    '<div>' +
      '<div class="profile-name">' + user.name + '</div>' +
      '<div class="profile-id">ID: ' + user.id + '</div>' +
      '<div class="profile-joined">Member since ' + formatDate(user.createdAt) + '</div>' +
    '</div>' +
  '</div>' +

  '<div class="data-grid">' +
    '<div class="data-card">' +
      '<div class="data-card-label">Email</div>' +
      '<div class="data-card-value">' + data.email + '</div>' +
    '</div>' +
    '<div class="data-card">' +
      '<div class="data-card-label">Phone</div>' +
      '<div class="data-card-value">' + data.phone + '</div>' +
    '</div>' +
    '<div class="data-card">' +
      '<div class="data-card-label">Age</div>' +
      '<div class="data-card-value">' + data.age + '</div>' +
    '</div>' +
    '<div class="data-card">' +
      '<div class="data-card-label">User ID</div>' +
      '<div class="data-card-value" style="font-size: 0.78rem; font-family: Courier New, monospace;">' + user.id + '</div>' +
    '</div>' +
  '</div>' +

  '<div class="profile-actions">' +
    '<a href="change-password.html" class="btn btn-secondary">Change Password</a>' +
    '<button class="btn btn-danger" id="cardLogoutBtn">Log Out</button>' +
  '</div>';

// Attach the logout listener to the card button (created above)
document.getElementById('cardLogoutBtn').addEventListener('click', logout);

// Attach the logout listener to the navbar button
document.getElementById('navLogoutBtn').addEventListener('click', logout);
