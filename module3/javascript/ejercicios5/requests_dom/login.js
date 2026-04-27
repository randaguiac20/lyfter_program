/**
 * login.js — Login page logic
 *
 * Receives User ID + password, calls API.verifyLogin() (backed by the same
 * localStorage DB used by register.js / API.postNewObject()).
 * Session is stored in localStorage so it persists across reloads/closes.
 */

(function () {
  // ── Auth guard: redirect to profile if already logged in ──────────────────
  if (Session.isLoggedIn()) {
    window.location.href = 'profile.html';
    return;
  }

  const form           = document.getElementById('loginForm');
  const alertBox        = document.getElementById('alert');
  const submitBtn       = document.getElementById('submitBtn');
  const userIdInput     = document.getElementById('userId');
  const rememberCheckbox = document.getElementById('rememberMe');

  const REMEMBER_KEY = 'lyfter_remember_id';

  // ── Remember Me: pre-fill on page load ─────────────────────────────────
  const savedId = localStorage.getItem(REMEMBER_KEY);
  if (savedId) {
    userIdInput.value = savedId;
    rememberCheckbox.checked = true;
  }

  // ── Helpers ───────────────────────────────────────────────────────────────

  function showAlert(message, type) {
    alertBox.className = `alert alert-${type}`;
    alertBox.textContent = message;
  }

  function hideAlert() {
    alertBox.className = 'alert hidden';
    alertBox.textContent = '';
  }

  function setFieldError(fieldId, message) {
    const input   = document.getElementById(fieldId);
    const errorEl = document.getElementById(`${fieldId}-error`);
    if (message) {
      input.classList.add('error');
      errorEl.textContent = message;
    } else {
      input.classList.remove('error');
      errorEl.textContent = '';
    }
  }

  function clearAllErrors() {
    ['userId', 'password'].forEach(f => setFieldError(f, ''));
    hideAlert();
  }

  function setLoading(loading) {
    submitBtn.disabled = loading;
    submitBtn.innerHTML = loading
      ? '<span class="spinner"></span> Logging in…'
      : 'Log In';
  }

  // ── Validation ────────────────────────────────────────────────────────────

  function validate(userId, password) {
    let valid = true;

    if (!userId.trim()) {
      setFieldError('userId', 'User ID is required.');
      valid = false;
    }

    if (!password) {
      setFieldError('password', 'Password is required.');
      valid = false;
    }

    return valid;
  }

  // ── Submit handler ────────────────────────────────────────────────────────

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    clearAllErrors();

    const userId   = userIdInput.value.trim();
    const password = document.getElementById('password').value;

    if (!validate(userId, password)) return;

    setLoading(true);

    try {
      // Verify against the same DB used at registration
      const user = await API.verifyLogin(userId, password);

      // Remember Me: save or clear the User ID based on checkbox state
      if (rememberCheckbox.checked) {
        localStorage.setItem(REMEMBER_KEY, userId);
      } else {
        localStorage.removeItem(REMEMBER_KEY);
      }

      // Persist session in localStorage (survives reloads and browser close)
      Session.save(user);

      // Redirect to My Profile
      window.location.href = 'profile.html';
    } catch (err) {
      setLoading(false);
      // API returns specific messages: "User not found" or "Incorrect password"
      const message = err.message || 'Login failed. Please try again.';
      showAlert(message, 'error');
    }
  });
})();
