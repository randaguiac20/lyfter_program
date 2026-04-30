// db.js — Real API Database
// Instead of using localStorage as a fake database, we now use restful-api.dev
// to store user data for real via HTTP requests.
//
// ── SETUP (do this once before running the app) ───────────────────────────
// 1. Go to https://restful-api.dev/ and log in to your account
// 2. Copy your API key from the dashboard and paste it in API_KEY below
// ─────────────────────────────────────────────────────────────────────────
//
// This file exposes 4 global functions that the other JS files can call:
//   getUsers()          - get all users (without passwords)
//   createUser()        - register a new user
//   loginUser()         - check login credentials
//   changePassword()    - update a user's password

var API_BASE = 'https://api.restful-api.dev';
var API_KEY = 'bfb54eb0-c07c-4dd6-a16a-435f26cbd5f8'; // <-- your API key from restful-api.dev/dashboard
var COLLECTION = 'lyfter_users';                       // the "table" name in the API

// ── Authenticated request ─────────────────────────────────────────────────

// A wrapper around axios that automatically adds the API key to every request.
// It returns response.data directly so callers get the already-parsed object.
function authFetch(url, options) {
  if (!options) {
    options = {};
  }

  return axios({
    method: options.method || 'GET',
    url: url,
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': API_KEY
    },
    data: options.body ? JSON.parse(options.body) : undefined
  }).then(function(response) {
    return response.data;
  }).catch(function(error) {
    // 403 means the API key is wrong or expired — get a new one from the dashboard
    if (error.response && error.response.status === 403) {
      throw { status: 403, message: 'API key is invalid. Get a fresh one from restful-api.dev/dashboard and update API_KEY in db.js.' };
    }
    throw error;
  });
}

// ── Public functions ──────────────────────────────────────────────────────

// GET all users — returns a Promise that resolves with a list of users.
// We never include the password in what we return (security!).
function getUsers() {
  return authFetch(API_BASE + '/collections/' + COLLECTION + '/objects')
    .catch(function(error) {
      // axios throws when the server returns 4xx/5xx.
      // A 404 here just means the collection is brand new (no users yet).
      if (error.response && error.response.status === 404) {
        return [];
      }
      throw error;
    })
    .then(function(objects) {
      var safeUsers = [];

      // Loop through every user and copy their info (without the password)
      for (var i = 0; i < objects.length; i++) {
        var obj = objects[i];
        if (obj.data) {
          safeUsers.push({
            id: obj.id,
            name: obj.name,
            data: {
              email: obj.data.email,
              phone: obj.data.phone,
              age: obj.data.age
            },
            createdAt: obj.data.createdAt || null
          });
        }
      }

      return safeUsers;
    });
}

// POST a new user (register).
// Expects an object like: { name, password, data: { email, phone, age } }
// Returns a Promise that resolves with the created user (without password).
function createUser(newUser) {
  // Step 1: get all users first so we can check for duplicate emails
  return authFetch(API_BASE + '/collections/' + COLLECTION + '/objects')
    .catch(function(error) {
      // 404 means the collection is empty — that is fine, no duplicates possible
      if (error.response && error.response.status === 404) {
        return [];
      }
      throw error;
    })
    .then(function(objects) {
      // Check if the email is already in use
      for (var i = 0; i < objects.length; i++) {
        if (objects[i].data && objects[i].data.email &&
            objects[i].data.email.toLowerCase() === newUser.data.email.toLowerCase()) {
          throw { status: 409, message: 'That email is already registered.' };
        }
      }

      // Step 2: send a POST request to create the user.
      // We store createdAt inside data because the API does not add it automatically.
      return authFetch(API_BASE + '/collections/' + COLLECTION + '/objects', {
        method: 'POST',
        body: JSON.stringify({
          name: newUser.name,
          data: {
            email: newUser.data.email,
            phone: newUser.data.phone,
            age: newUser.data.age,
            password: newUser.password,
            createdAt: new Date().toISOString()
          }
        })
      });
    })
    .then(function(created) {
      console.log('User created:', created.id);

      // Return the user WITHOUT the password
      return {
        id: created.id,
        name: created.name,
        data: {
          email: created.data.email,
          phone: created.data.phone,
          age: created.data.age
        },
        createdAt: created.data.createdAt
      };
    });
}

// GET a single user by their ID and verify their password (login).
// Returns a Promise that resolves with the user (without password) if correct.
function loginUser(userId, password) {
  return authFetch(API_BASE + '/collections/' + COLLECTION + '/objects/' + userId)
    .catch(function(error) {
      // axios throws on 404 — translate it into a friendly message
      if (error.response && error.response.status === 404) {
        throw { status: 404, message: 'User not found. Please check your ID.' };
      }
      throw error;
    })
    .then(function(obj) {
      // Check if the password matches
      if (obj.data.password !== password) {
        throw { status: 401, message: 'Incorrect password. Please try again.' };
      }

      // Return the user WITHOUT the password
      return {
        id: obj.id,
        name: obj.name,
        data: {
          email: obj.data.email,
          phone: obj.data.phone,
          age: obj.data.age
        },
        createdAt: obj.data.createdAt
      };
    });
}

// Update a user's password.
// First fetches the user to verify the old password, then PATCHes with the new one.
function changePassword(userId, oldPassword, newPassword) {
  // Step 1: get the current user data from the API
  return authFetch(API_BASE + '/collections/' + COLLECTION + '/objects/' + userId)
    .catch(function(error) {
      if (error.response && error.response.status === 404) {
        throw { status: 404, message: 'User not found. Please check your ID.' };
      }
      throw error;
    })
    .then(function(obj) {
      // Step 2: check that the old password is correct
      if (obj.data.password !== oldPassword) {
        throw { status: 401, message: 'Current password is incorrect.' };
      }

      // Step 3: send a PATCH request with the updated password.
      // We include ALL data fields so nothing gets lost.
      return authFetch(API_BASE + '/collections/' + COLLECTION + '/objects/' + userId, {
        method: 'PATCH',
        body: JSON.stringify({
          name: obj.name,
          data: {
            email: obj.data.email,
            phone: obj.data.phone,
            age: obj.data.age,
            password: newPassword,
            createdAt: obj.data.createdAt
          }
        })
      });
    })
    .then(function() {
      return { message: 'Password updated successfully.' };
    });
}
