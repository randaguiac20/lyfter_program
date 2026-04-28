/**
 * session.js — Session Manager
 * Persists the logged-in user in localStorage so the session survives
 * page reloads and browser close/reopen.
 */

const Session = (() => {
  const KEY = 'lyfter_session';

  /** Save user object to session (call after register or login). */
  function save(user) {
    localStorage.setItem(KEY, JSON.stringify(user));
  }

  /** Get the current session user, or null if not logged in. */
  function get() {
    const raw = localStorage.getItem(KEY);
    return raw ? JSON.parse(raw) : null;
  }

  /** Clear the session (logout). */
  function clear() {
    localStorage.removeItem(KEY);
  }

  /** Returns true if a session exists. */
  function isLoggedIn() {
    return get() !== null;
  }

  return { save, get, clear, isLoggedIn };
})();
