/**
 * db.js — Dummy API
 * Simulates a REST API using localStorage as the data store.
 * Mirrors the exact logic pattern from axios_exercise2.js:
 *   - getObjects()       → GET  /objects (filters those without `data`)
 *   - postNewObject()    → POST /objects (creates a new user with auto-generated ID)
 *   - verifyLogin()      → Verifies ID + password
 *   - updateUserPassword() → Updates a user's password
 *
 * Data shape (mirrors axios_exercise2.js structure):
 *   { id, name, password, data: { email, phone, age }, createdAt }
 */

const API = (() => {
  const STORAGE_KEY = 'lyfter_users';
  const DELAY = 400; // Simulate network latency (ms)

  // ── Private helpers ──────────────────────────────────────────────────────────

  function _getUsers() {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  }

  function _saveUsers(users) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(users));
  }

  function _generateId() {
    const timestamp = Date.now().toString(36).toUpperCase();
    const random = Math.random().toString(36).substring(2, 7).toUpperCase();
    return `USR-${timestamp}-${random}`;
  }

  // ── Public API ───────────────────────────────────────────────────────────────

  /**
   * GET /objects
   * Returns all users that have a `data` field (same filter logic as exercise 2).
   * Passwords are never exposed.
   */
  function getObjects() {
    console.log('Loading objects...');
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          const users = _getUsers();
          console.log('Data loaded! Returning...');
          // Only users with data are added to the filetered var
          const filtered = users.filter(u => u.data);
          // These a 3 steps compact code
          // It basically removes key password from the dataset
          resolve(filtered.map(({ password, ...safe }) => safe));
        } catch (err) {
          console.log('Error fetching objects:', err);
          reject({ status: 500, message: 'Internal error fetching objects.' });
        }
      }, DELAY);
    });
  }

  /**
   * POST /objects
   * Creates a new user object >> postNewObject(newObject).
   * Expected shape: { name, password, data: { email, phone, age } }
   */
  function postNewObject(newObject) {
    console.log('Posting new object');
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          if (!newObject.name || !newObject.password || !newObject.data) {
            reject({ status: 400, message: 'Missing required fields.' });
            return;
          }

          const users = _getUsers();

          // Enforce unique email
          const emailExists = users.some(
            u => u.data?.email?.toLowerCase() === newObject.data?.email?.toLowerCase()
          );
          if (emailExists) {
            reject({ status: 409, message: 'This email is already registered.' });
            return;
          }

          const user = {
            id: _generateId(),
            name: newObject.name,
            password: newObject.password,
            data: newObject.data,
            createdAt: new Date().toISOString()
          };
          // Append data for new user
          users.push(user);
          // Create new user
          _saveUsers(users);

          // Never return password — mirrors a real API response
          const { password, ...safeUser } = user;
          console.log('Object created:', safeUser);
          console.log('POST is done.');
          resolve(safeUser);
        } catch (err) {
          console.log('Error creating object:', err);
          reject({ status: 500, message: 'Internal error creating user.' });
        }
      }, DELAY);
    });
  }

  /**
   * Verifies login credentials by ID + password.
   * Returns the user object (without password) if valid.
   */
  function verifyLogin(id, password) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          const users = _getUsers();
          const user = users.find(u => u.id === id);

          if (!user) {
            reject({ status: 404, message: 'User not found. Please check your ID.' });
            return;
          }
          if (user.password !== password) {
            reject({ status: 401, message: 'Incorrect password. Please try again.' });
            return;
          }

          const { password: _, ...safeUser } = user;
          resolve(safeUser);
        } catch (err) {
          reject({ status: 500, message: 'Internal error during login.' });
        }
      }, DELAY);
    });
  }

  /**
   * Updates a user's password after verifying the old one.
   */
  function updateUserPassword(id, oldPassword, newPassword) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        try {
          const users = _getUsers();
          const user_index_id = users.findIndex(u => u.id === id);

          if (user_index_id === -1) {
            reject({ status: 404, message: 'User not found. Please check your ID.' });
            return;
          }
          if (users[user_index_id].password !== oldPassword) {
            reject({ status: 401, message: 'Current password is incorrect.' });
            return;
          }

          users[user_index_id].password = newPassword;
          _saveUsers(users);
          resolve({ message: 'Password updated successfully.' });
        } catch (err) {
          reject({ status: 500, message: 'Internal error updating password.' });
        }
      }, DELAY);
    });
  }

  return { getObjects, postNewObject, verifyLogin, updateUserPassword };
})();
