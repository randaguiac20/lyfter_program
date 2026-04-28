// db.js — Fake Database
// We use the browser's localStorage as if it were a database.
// All users are stored as a JSON array under the key 'lyfter_users'.
//
// This file exposes 4 global functions that the other JS files can call:
//   getUsers()          - get all users (without passwords)
//   createUser()        - register a new user
//   loginUser()         - check login credentials
//   changePassword()    - update a user's password

var USERS_KEY = 'lyfter_users';

// ── Private helpers (only used inside this file) ──────────────────────────

// Read the user list from localStorage.
// If nothing is saved yet, return an empty array.
function readUsers() {
  var stored = localStorage.getItem(USERS_KEY);
  if (stored === null) {
    return [];
  }
  return JSON.parse(stored);
}

// Save the updated user list back to localStorage.
function writeUsers(users) {
  localStorage.setItem(USERS_KEY, JSON.stringify(users));
}

// Create a unique ID for a new user.
// Example result: "USR-M3F2KX1A-HJ7QP"
function makeUserId() {
  var timestamp = Date.now().toString(36).toUpperCase();
  var randomPart = Math.random().toString(36).substring(2, 7).toUpperCase();
  return 'USR-' + timestamp + '-' + randomPart;
}

// ── Public functions ──────────────────────────────────────────────────────

// GET all users — returns a Promise that resolves with a list of users.
// We never include the password in what we return (security!).
// The setTimeout simulates a real network request taking 400ms.
function getUsers() {
  return new Promise(function(resolve, reject) {
    setTimeout(function() {
      var users = readUsers();
      var safeUsers = [];

      // Loop through every user and copy their info (without the password)
      for (var i = 0; i < users.length; i++) {
        var u = users[i];
        if (u.data) {
          var safeUser = {
            id: u.id,
            name: u.name,
            data: u.data,
            createdAt: u.createdAt
          };
          safeUsers.push(safeUser);
        }
      }

      resolve(safeUsers);
    }, 400);
  });
}

// POST a new user (register).
// Expects an object like: { name, password, data: { email, phone, age } }
// Returns a Promise that resolves with the created user (without password).
function createUser(newUser) {
  return new Promise(function(resolve, reject) {
    setTimeout(function() {
      // Make sure all required fields are present
      if (!newUser.name || !newUser.password || !newUser.data) {
        reject({ status: 400, message: 'Please fill in all required fields.' });
        return;
      }

      var users = readUsers();

      // Check if the email is already in use
      for (var i = 0; i < users.length; i++) {
        if (users[i].data && users[i].data.email.toLowerCase() === newUser.data.email.toLowerCase()) {
          reject({ status: 409, message: 'That email is already registered.' });
          return;
        }
      }

      // Build the new user object
      var user = {
        id: makeUserId(),
        name: newUser.name,
        password: newUser.password,
        data: newUser.data,
        createdAt: new Date().toISOString()
      };

      // Save to localStorage
      users.push(user);
      writeUsers(users);

      // Return the user WITHOUT the password
      var safeUser = {
        id: user.id,
        name: user.name,
        data: user.data,
        createdAt: user.createdAt
      };

      console.log('User created:', safeUser.id);
      resolve(safeUser);
    }, 400);
  });
}

// Verify login credentials (User ID + password).
// Returns a Promise that resolves with the user (without password) if correct.
function loginUser(userId, password) {
  return new Promise(function(resolve, reject) {
    setTimeout(function() {
      var users = readUsers();
      var foundUser = null;

      // Search for the user by their ID
      for (var i = 0; i < users.length; i++) {
        if (users[i].id === userId) {
          foundUser = users[i];
          break;
        }
      }

      // User not found
      if (foundUser === null) {
        reject({ status: 404, message: 'User not found. Please check your ID.' });
        return;
      }

      // Password is wrong
      if (foundUser.password !== password) {
        reject({ status: 401, message: 'Incorrect password. Please try again.' });
        return;
      }

      // Everything is correct — return the user WITHOUT the password
      var safeUser = {
        id: foundUser.id,
        name: foundUser.name,
        data: foundUser.data,
        createdAt: foundUser.createdAt
      };

      resolve(safeUser);
    }, 400);
  });
}

// Update a user's password.
// First checks that the old password is correct, then saves the new one.
function changePassword(userId, oldPassword, newPassword) {
  return new Promise(function(resolve, reject) {
    setTimeout(function() {
      var users = readUsers();
      var userIndex = -1;

      // Find the user's position in the array
      for (var i = 0; i < users.length; i++) {
        if (users[i].id === userId) {
          userIndex = i;
          break;
        }
      }

      // User not found
      if (userIndex === -1) {
        reject({ status: 404, message: 'User not found. Please check your ID.' });
        return;
      }

      // Old password does not match
      if (users[userIndex].password !== oldPassword) {
        reject({ status: 401, message: 'Current password is incorrect.' });
        return;
      }

      // Update the password and save
      users[userIndex].password = newPassword;
      writeUsers(users);

      resolve({ message: 'Password updated successfully.' });
    }, 400);
  });
}
