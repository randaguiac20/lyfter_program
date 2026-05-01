/**
 * change-password.js — Change Password page logic
 *
 * Validates:
 *   1. All fields are filled
 *   2. New password meets minimum length
 *   3. New password matches confirmation
 * Then calls API.updateUserPassword() which verifies:
 *   - User exists (status 404 if not)
 *   - Old password is correct (status 401 if not)
 * If the logged-in user changes their own password, the session is cleared
 * and they are redirected to login after a brief success message.
 */

(function () {
  const form      = document.getElementById('changePasswordForm');
  const alertBox  = document.getElementById('alert');
  const submitBtn = document.getElementById('submitBtn');
  const navLinks  = document.getElementById('navLinks');
  const userIdInput = document.getElementById('userId');

  // ── Navbar: adapt to session state ────────────────────────────────────────
  const session = Session.get();

  if (session) {
    // Pre-fill User ID for convenience
    userIdInput.value = session.id;

    navLinks.innerHTML = `
      <a href="profile.html">My Profile</a>
      <button id="navLogoutBtn">Log Out</button>
    `;
    document.getElementById('navLogoutBtn').addEventListener('click', function () {
      Session.clear();
      window.location.href = 'login.html';
    });
  } else {
    navLinks.innerHTML = `
      <a href="register.html">Register</a>
      <a href="login.html">Login</a>
    `;
  }

  // ── Helpers ───────────────────────────────────────────────────────────────

  function showAlert(message, type) {
    alertBox.className = `alert alert-${type}`;
    alertBox.textContent = message;
    alertBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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
    ['userId', 'oldPassword', 'newPassword', 'confirmPassword'].forEach(f => setFieldError(f, ''));
    hideAlert();
  }

  function setLoading(loading) {
    submitBtn.disabled = loading;
    submitBtn.innerHTML = loading
      ? '<span class="spinner"></span> Updating…'
      : 'Update Password';
  }

  // ── Validation (client-side) ──────────────────────────────────────────────

  function validate(fields) {
    let valid = true;

    if (!fields.userId.trim()) {
      setFieldError('userId', 'User ID is required.');
      valid = false;
    }

    if (!fields.oldPassword) {
      setFieldError('oldPassword', 'Current password is required.');
      valid = false;
    }

    if (!fields.newPassword) {
      setFieldError('newPassword', 'New password is required.');
      valid = false;
    } else if (fields.newPassword.length < 6) {
      setFieldError('newPassword', 'New password must be at least 6 characters.');
      valid = false;
    }

    if (!fields.confirmPassword) {
      setFieldError('confirmPassword', 'Please confirm your new password.');
      valid = false;
    } else if (fields.newPassword !== fields.confirmPassword) {
      setFieldError('confirmPassword', 'Passwords do not match.');
      valid = false;
    }

    return valid;
  }

  // ── Submit handler ────────────────────────────────────────────────────────

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    clearAllErrors();

    const fields = {
      userId:          document.getElementById('userId').value.trim(),
      oldPassword:     document.getElementById('oldPassword').value,
      newPassword:     document.getElementById('newPassword').value,
      confirmPassword: document.getElementById('confirmPassword').value,
    };

    if (!validate(fields)) return;

    setLoading(true);

    try {
      // API validates: user exists + old password correct
      await API.updateUserPassword(fields.userId, fields.oldPassword, fields.newPassword);

      showAlert('Password updated successfully!', 'success');
      form.reset();

      // If the logged-in user just changed their own password, clear session
      // and redirect to login so they authenticate with the new password.
      if (session && session.id === fields.userId) {
        Session.clear();
        showAlert('Password updated! Redirecting to login…', 'success');
        setTimeout(() => {
          window.location.href = 'login.html';
        }, 2000);
      } else {
        // Not the current user — keep ID pre-filled if it was
        if (session) userIdInput.value = session.id;
      }
    } catch (err) {
      // API returns specific messages: "User not found" or "Current password is incorrect"
      const message = err.message || 'Failed to update password. Please try again.';
      showAlert(message, 'error');
    } finally {
      setLoading(false);
    }
  });
})();
