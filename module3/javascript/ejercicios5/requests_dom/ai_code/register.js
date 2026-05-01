/**
 * register.js — Register page logic
 *
 * Uses the same postNewObject() logic from axios_exercise2.js:
 *   - Builds an object with shape { name, data: { ... } }
 *   - Calls API.postNewObject() which mirrors the exercise's POST function
 * Session is stored in localStorage so it persists across reloads/closes.
 * We are making use of "Immediately Invoked Function Expression" (IIFE)
 */

(function () {
  // ── Auth guard: redirect to profile if already logged in ──────────────────
  if (Session.isLoggedIn()) {
    window.location.href = 'profile.html';
    return;
  }

  const form      = document.getElementById('registerForm');
  const alertBox  = document.getElementById('alert');
  const submitButton = document.getElementById('submitButton');

  const FIELDS = ['name', 'email', 'phone', 'age', 'password', 'confirmPassword'];

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
    const errorElement = document.getElementById(`${fieldId}-error`);
    if (message) {
      input.classList.add('error');
      errorElement.textContent = message;
    } else {
      input.classList.remove('error');
      errorElement.textContent = '';
    }
  }

  function clearAllErrors() {
    FIELDS.forEach(f => setFieldError(f, ''));
    hideAlert();
  }

  function setLoading(loading) {
    submitButton.disabled = loading;
    submitButton.innerHTML = loading
      ? '<span class="spinner"></span> Creating account…'
      : 'Create Account';
  }

  // ── Success modal ─────────────────────────────────────────────────────────

  /**
   * Replaces the native alert() so the user can copy their ID.
   * Injects an overlay modal with the ID in a selectable box and a
   * one-click "Copy ID" button. Redirects to profile.html on continue.
   */
  function showSuccessModal(userId) {
    // Build modal markup and inject into <body>
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-labelledby', 'modal-title');

    overlay.innerHTML = `
      <div class="modal-box">
        <div class="modal-icon">✓</div>
        <h2 class="modal-title" id="modal-title">User was created correctly!</h2>
        <p class="modal-subtitle">Save your User ID — you will need it to log in.</p>
        <div class="modal-id-box">
          <span class="modal-id-value" id="modalIdValue">${userId}</span>
          <button class="btn-copy" id="copyIdBtn" type="button">Copy ID</button>
        </div>
        <div class="modal-actions">
          <button class="btn btn-primary" id="continueBtn" type="button">Continue to Profile →</button>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);

    // Copy button logic
    const copyButton = document.getElementById('copyIdBtn');
    copyButton.addEventListener('click', function () {
      navigator.clipboard.writeText(userId).then(() => {
        copyButton.textContent = 'Copied!';
        copyButton.classList.add('copied');
        setTimeout(() => {
          copyButton.textContent = 'Copy ID';
          copyButton.classList.remove('copied');
        }, 2000);
      }).catch(() => {
        // Fallback for browsers that block clipboard on file:// origin
        const el = document.getElementById('modalIdValue');
        const range = document.createRange();
        range.selectNodeContents(el);
        const sel = window.getSelection();
        sel.removeAllRanges();
        sel.addRange(range);
        copyButton.textContent = 'Selected!';
        setTimeout(() => { copyButton.textContent = 'Copy ID'; }, 2000);
      });
    });

    // Continue button → redirect
    document.getElementById('continueBtn').addEventListener('click', function () {
      window.location.href = 'profile.html';
    });
  }

  // ── Validation ────────────────────────────────────────────────────────────

  function validate(fields) {
    let valid = true;
    const emailRx = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!fields.name.trim()) {
      setFieldError('name', 'Full name is required.');
      valid = false;
    }

    if (!fields.email.trim()) {
      setFieldError('email', 'Email is required.');
      valid = false;
    } else if (!emailRx.test(fields.email)) {
      setFieldError('email', 'Please enter a valid email address.');
      valid = false;
    }

    if (!fields.phone.trim()) {
      setFieldError('phone', 'Phone number is required.');
      valid = false;
    }

    const ageNum = parseInt(fields.age, 10);
    if (!fields.age) {
      setFieldError('age', 'Age is required.');
      valid = false;
    } else if (isNaN(ageNum) || ageNum < 1 || ageNum > 120) {
      setFieldError('age', 'Please enter a valid age between 1 and 120.');
      valid = false;
    }

    if (!fields.password) {
      setFieldError('password', 'Password is required.');
      valid = false;
    } else if (fields.password.length < 6) {
      setFieldError('password', 'Password must be at least 6 characters long.');
      valid = false;
    }

    if (!fields.confirmPassword) {
      setFieldError('confirmPassword', 'Please confirm your password.');
      valid = false;
    } else if (fields.password !== fields.confirmPassword) {
      setFieldError('confirmPassword', 'Passwords do not match.');
      valid = false;
    }

    return valid;
  }

  // ── Submit handler ────────────────────────────────────────────────────────

  form.addEventListener('submit', async function (event) {
    event.preventDefault();
    clearAllErrors();

    const fields = {
      name:            document.getElementById('name').value.trim(),
      email:           document.getElementById('email').value.trim(),
      phone:           document.getElementById('phone').value.trim(),
      age:             document.getElementById('age').value,
      password:        document.getElementById('password').value,
      confirmPassword: document.getElementById('confirmPassword').value,
    };

    if (!validate(fields)) return;

    setLoading(true);

    /**
     * Build the new object following axios_exercise2.js structure:
     *   { name, data: { ... } }
     * This mirrors exactly what postNewObject() expects.
     */
    const newObject = {
      name:     fields.name,
      password: fields.password,
      data: {
        email: fields.email,
        phone: fields.phone,
        age:   parseInt(fields.age, 10),
      },
    };

    try {
      // Mirrors axios_exercise2.js: await postNewObject(newObject)
      const createdUser = await API.postNewObject(newObject);

      // Persist session in localStorage (survives reloads and browser close)
      Session.save(createdUser);

      // Show custom modal (replaces native alert — allows copy-paste of ID)
      setLoading(false);
      showSuccessModal(createdUser.id);
    } catch (err) {
      setLoading(false);
      const message = err.message || 'An unexpected error occurred. Please try again.';
      showAlert(`Registration failed: ${message}`, 'error');
    }
  });
})();
