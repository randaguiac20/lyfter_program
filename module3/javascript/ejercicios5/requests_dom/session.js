// session.js — Session Manager
// Keeps track of who is currently logged in.
// We store the logged-in user as JSON in localStorage so the session
// survives page refreshes and even closing the browser tab.
//
// This file exposes 4 global functions:
//   saveSession(user)  - save the user after login/register
//   getSession()       - get the current user (or null if not logged in)
//   clearSession()     - remove the session (logout)
//   isLoggedIn()       - returns true if a session exists

var SESSION_KEY = 'lyfter_session';

// Save the logged-in user to localStorage
function saveSession(user) {
  localStorage.setItem(SESSION_KEY, JSON.stringify(user));
}

// Get the current logged-in user.
// Returns the user object, or null if nobody is logged in.
function getSession() {
  var stored = localStorage.getItem(SESSION_KEY);
  if (stored === null) {
    return null;
  }
  return JSON.parse(stored);
}

// Remove the session — used when the user logs out
function clearSession() {
  localStorage.removeItem(SESSION_KEY);
}

// Returns true if someone is logged in, false otherwise
function isLoggedIn() {
  return getSession() !== null;
}
