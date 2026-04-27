/**
 * profile.js — My Profile page logic
 *
 * Auth guard: redirects to login.html if no active session.
 * Renders user data (returned by API.postNewObject / stored in session)
 * as info cards. Provides a logout button that clears the session.
 */

(function () {
  // ── Auth guard ────────────────────────────────────────────────────────────
  if (!Session.isLoggedIn()) {
    window.location.href = 'login.html';
    return;
  }

  const user         = Session.get();
  const profileCard  = document.getElementById('profileCard');
  const navLogoutBtn = document.getElementById('navLogoutBtn');

  // ── Helpers ───────────────────────────────────────────────────────────────

  function getInitials(name) {
    return (name || '?')
      .split(' ')
      .map(w => w[0])
      .slice(0, 2)
      .join('')
      .toUpperCase();
  }

  function formatDate(isoString) {
    if (!isoString) return 'N/A';
    return new Date(isoString).toLocaleDateString('en-US', {
      year: 'numeric', month: 'long', day: 'numeric',
    });
  }

  function logout() {
    Session.clear();
    window.location.href = 'login.html';
  }

  // ── Render ────────────────────────────────────────────────────────────────

  function render() {
    const data = user.data || {};

    profileCard.innerHTML = `
      <div class="profile-header">
        <div class="avatar">${getInitials(user.name)}</div>
        <div>
          <div class="profile-name">${user.name}</div>
          <div class="profile-id">ID: ${user.id}</div>
          <div class="profile-joined">Member since ${formatDate(user.createdAt)}</div>
        </div>
      </div>

      <div class="data-grid">
        <div class="data-card">
          <div class="data-card-label">Email</div>
          <div class="data-card-value">${data.email || 'N/A'}</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Phone</div>
          <div class="data-card-value">${data.phone || 'N/A'}</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">Age</div>
          <div class="data-card-value">${data.age || 'N/A'}</div>
        </div>
        <div class="data-card">
          <div class="data-card-label">User ID</div>
          <div class="data-card-value" style="font-size:.82rem; font-family:'Courier New',monospace;">${user.id}</div>
        </div>
      </div>

      <div class="profile-actions">
        <a href="change-password.html" class="btn btn-secondary">Change Password</a>
        <button class="btn btn-danger" id="cardLogoutBtn">Log Out</button>
      </div>
    `;

    document.getElementById('cardLogoutBtn').addEventListener('click', logout);
  }

  // ── Init ──────────────────────────────────────────────────────────────────
  navLogoutBtn.addEventListener('click', logout);
  render();
})();
