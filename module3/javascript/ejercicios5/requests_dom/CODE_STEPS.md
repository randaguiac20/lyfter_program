# Lyfter — `requests_dom` Codebase Walkthrough

> **What this project is:** A fully client-side, multi-page user-auth mini-app built with vanilla JavaScript, HTML, and CSS. There is no backend server. Instead, `localStorage` acts as the database and `Promise`-based functions simulate async API calls (mimicking the axios patterns practiced in earlier exercises). The project demonstrates DOM manipulation, form validation, session management, and simulated REST API interaction entirely in the browser.

---

## Table of Contents

1. [File Map](#1-file-map)
2. [Architecture Overview](#2-architecture-overview)
3. [General Workflow](#3-general-workflow)
4. [Detailed Step-by-Step Flow — Every File](#4-detailed-step-by-step-flow--every-file)
   - 4.1 [styles.css](#41-stylescss)
   - 4.2 [db.js — The Fake API](#42-dbjs--the-fake-api)
   - 4.3 [session.js — Session Manager](#43-sessionjs--session-manager)
   - 4.4 [register.html + register.js — Registration Page](#44-registerhtml--registerjs--registration-page)
   - 4.5 [login.html + login.js — Login Page](#45-loginhtml--loginjs--login-page)
   - 4.6 [profile.html + profile.js — Profile Page](#46-profilehtml--profilejs--profile-page)
   - 4.7 [change-password.html + change-password.js — Change Password Page](#47-change-passwordhtml--change-passwordjs--change-password-page)
5. [Data Shapes](#5-data-shapes)
6. [localStorage Keys Reference](#6-localstorage-keys-reference)
7. [Security & Design Decisions](#7-security--design-decisions)

---

## 1. File Map

```
requests_dom/
├── styles.css              ← Shared stylesheet for all pages
├── db.js                   ← Fake API (localStorage as database)
├── session.js              ← Session manager (read/write/clear session)
│
├── register.html           ← Registration form markup
├── register.js             ← Registration form logic
│
├── login.html              ← Login form markup
├── login.js                ← Login form logic
│
├── profile.html            ← Authenticated user profile page markup
├── profile.js              ← Profile rendering + logout logic
│
├── change-password.html    ← Change-password form markup
└── change-password.js      ← Change-password form logic
```

**Script load order on every page** (declared at bottom of each HTML `<body>`):

```
db.js  →  session.js  →  [page-specific].js
```

`db.js` and `session.js` must always be loaded first because the page scripts depend on the `API` and `Session` globals they expose.

---

## 2. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        BROWSER                              │
│                                                             │
│  ┌────────────┐   ┌────────────┐   ┌──────────────────────┐│
│  │ HTML Pages │   │  JS Logic  │   │     localStorage     ││
│  │            │   │            │   │                      ││
│  │ register   │──▶│ register.js│   │  lyfter_users  []    ││
│  │ login      │──▶│ login.js   │◀─▶│  lyfter_session {}  ││
│  │ profile    │──▶│ profile.js │   │  lyfter_remember_id  ││
│  │ change-pwd │──▶│ chg-pwd.js │   └──────────────────────┘│
│  └────────────┘   └─────┬──────┘              ▲            │
│                         │                     │            │
│                   ┌─────▼──────┐       ┌──────┴──────┐    │
│                   │  session.js│       │    db.js    │    │
│                   │  Session{} │       │    API{}    │    │
│                   └────────────┘       └─────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

- **`db.js`** exposes a global `API` object that wraps all `localStorage` read/write operations inside `Promise + setTimeout` to simulate real network latency (400 ms). It is the single source of truth for user data.
- **`session.js`** exposes a global `Session` object that stores the currently logged-in user as a JSON blob under a separate localStorage key. It is intentionally separate from the user database so that reading "who is logged in" never requires a DB scan.
- **Page scripts** are each wrapped in an IIFE `(function(){ ... })()` to avoid polluting the global scope. They read from `Session` and `API`, manipulate the DOM, and redirect the browser when auth state changes.
- **`styles.css`** is a single shared stylesheet imported by every page; it uses CSS custom properties (variables) for consistent theming.

---

## 3. General Workflow

```
  ┌──────────────────────────────────────────────────────┐
  │                  New User Journey                    │
  │                                                      │
  │  1. Open register.html                               │
  │     → Fill out form (name, email, phone, age,        │
  │       password, confirmPassword)                     │
  │     → Client-side validation runs                    │
  │     → API.postNewObject() saves user to localStorage │
  │     → Success modal shows User ID                    │
  │     → Session is saved → redirect to profile.html    │
  │                                                      │
  │  2. profile.html                                     │
  │     → Auth guard reads Session; redirects to login   │
  │       if no session                                  │
  │     → Renders user info cards (name, email,          │
  │       phone, age, ID, join date)                     │
  │     → Logout clears session → redirect to login      │
  └──────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────┐
  │               Returning User Journey                 │
  │                                                      │
  │  1. Open login.html                                  │
  │     → Enter User ID + password                       │
  │     → API.verifyLogin() checks localStorage DB       │
  │     → Session saved → redirect to profile.html       │
  │                                                      │
  │  2. profile.html (same as above)                     │
  └──────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────┐
  │             Change Password Journey                  │
  │                                                      │
  │  1. Open change-password.html (from profile or       │
  │     login's "Forgot?" link)                          │
  │     → Enter User ID, current password, new password  │
  │     → API.updateUserPassword() verifies + updates DB │
  │     → If it was the logged-in user's own password,   │
  │       session is cleared → redirect to login         │
  └──────────────────────────────────────────────────────┘
```

**Navigation rules (auth guards):**

| Page                   | Logged In                               | Not Logged In                       |
| ---------------------- | --------------------------------------- | ----------------------------------- |
| `register.html`        | Redirect → `profile.html`               | Show form                           |
| `login.html`           | Redirect → `profile.html`               | Show form                           |
| `profile.html`         | Show profile                            | Redirect → `login.html`             |
| `change-password.html` | Pre-fill User ID; show logout in navbar | Show register/login links in navbar |

---

## 4. Detailed Step-by-Step Flow — Every File

---

### 4.1 `styles.css`

**Purpose:** Single shared stylesheet. No page-specific files — all pages import only this one. This keeps the visual language consistent and avoids duplication.

#### CSS Custom Properties (`:root`)

Defined at the top so every rule can reference them by name instead of hard-coding hex values or numbers:

```css
:root {
  --primary: #4f46e5; /* Indigo — used for buttons, links, focus rings */
  --primary-dark: #3730a3; /* Darker indigo for hover states */
  --primary-light: #818cf8; /* Light indigo — used in avatar gradient */
  --success: #16a34a; /* Green text for success messages */
  --success-bg: #dcfce7; /* Green background for success alert box */
  --error: #dc2626; /* Red text + border for error states */
  --text-primary: #111827; /* Near-black body text */
  --text-secondary: #6b7280; /* Gray subtitles */
  --text-muted: #9ca3af; /* Lighter gray for labels, placeholders */
  --border: #e5e7eb; /* Light border for inputs, cards, dividers */
  --bg: #f3f4f6; /* Page background (off-white) */
  --radius: 8px; /* Standard border-radius */
  --radius-lg: 14px; /* Larger radius for cards/modals */
}
```

#### Key Component Blocks

| Block                                                   | What it does                                                                                                                                                          |
| ------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `body`                                                  | Sets system font stack, background, and `min-height: 100vh` so short pages still fill the screen                                                                      |
| `.navbar`                                               | Sticky top bar, indigo background, flexbox layout with brand on left and links on right                                                                               |
| `.page`                                                 | Full-height centering wrapper — uses `display: flex; align-items: center; justify-content: center` so the card is always vertically centered                          |
| `.card`                                                 | White rounded box with `box-shadow` — the visual container for all forms and profile content. `.card-wide` variant expands `max-width` to 680 px for the profile page |
| `.form-group`                                           | Vertical stack of label + input + error span with consistent spacing                                                                                                  |
| `input:focus`                                           | Shows a `box-shadow` focus ring in indigo (accessible, visible without changing the layout)                                                                           |
| `input.error`                                           | Red border + red shadow — applied by JS when validation fails                                                                                                         |
| `.field-error`                                          | Small red text block below each input; always present in the DOM (with `min-height`) so the form doesn't jump when errors appear                                      |
| `.btn`, `.btn-primary`, `.btn-secondary`, `.btn-danger` | Unified button styles; `:disabled` reduces opacity and blocks interaction                                                                                             |
| `.alert`, `.alert-error`, `.alert-success`              | Global feedback banner above the form; uses `animation: fadeSlideIn` for smooth entry                                                                                 |
| `.spinner`                                              | CSS-only spinning ring via `border-top-color` trick — shown inside the submit button while an async call is in flight                                                 |
| `.modal-overlay` / `.modal-box`                         | Fixed full-screen overlay with a centred white card — used by the registration success modal                                                                          |
| `.modal-id-box` / `.btn-copy` / `.btn-copy.copied`      | ID display area with a copy button that turns green when clicked                                                                                                      |
| `.profile-header` / `.avatar`                           | Flex row with a circular gradient avatar and name/ID/join-date stack                                                                                                  |
| `.data-grid` / `.data-card`                             | 2-column CSS Grid of info cards for email, phone, age, and User ID on the profile page                                                                                |
| `@keyframes fadeSlideIn`                                | Slides alerts in from 6 px above with a fade — prevents jarring pop-in                                                                                                |
| `@keyframes spin`                                       | Rotates the spinner continuously                                                                                                                                      |

---

### 4.2 `db.js` — The Fake API

**Purpose:** Replaces a real REST API with a `localStorage`-backed simulation. All four operations return Promises that resolve or reject after a 400 ms `setTimeout` to simulate network latency. This mirrors the axios pattern used in earlier exercises (`axios_exercise2.js`), so the page scripts can use `async/await` exactly as they would against a real server.

#### The IIFE module pattern

```js
const API = (() => { ... return { ... }; })();
```

Everything is wrapped in an Immediately Invoked Function Expression. Only the four public methods are returned and exposed on the `API` global. The storage key, delay constant, and helper functions are private — they cannot be accessed or tampered with from the browser console.

#### Private helpers

| Helper              | Role                                                                                                                                                                                               |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `_getUsers()`       | Reads `lyfter_users` from localStorage and parses the JSON array. Returns `[]` if nothing is stored yet                                                                                            |
| `_saveUsers(users)` | Serialises the array back to JSON and writes it to localStorage                                                                                                                                    |
| `_generateId()`     | Generates a unique user ID in the format `USR-<timestamp base-36>-<random base-36>` (e.g. `USR-LX2A4B-K9F3J`). Uses `Date.now().toString(36)` for uniqueness and `Math.random()` for extra entropy |

#### Public methods

##### `getObjects()`

```
Simulates: GET /objects
```

- Reads all users from localStorage.
- **Filters out** any users that do not have a `data` field (mirrors the filter logic in `axios_exercise2.js`).
- **Strips passwords** from every returned object using destructuring: `const { password, ...safe } = user`.
- Resolves with the safe array; rejects with a 500-status error object if localStorage throws.
- Used by: not called by any page script in this app currently — it exists to complete the API mirror pattern and could be used to display a user list.

##### `postNewObject(newObject)`

```
Simulates: POST /objects
Expected input: { name, password, data: { email, phone, age } }
```

- Validates that `name`, `password`, and `data` are all present; rejects with status 400 if not.
- **Enforces unique email** — scans all existing users for a case-insensitive match; rejects with status 409 (`"This email is already registered."`) if found.
- Generates a new ID via `_generateId()` and attaches a `createdAt` ISO timestamp.
- Pushes the full user object (including the password) to the array and saves it.
- Resolves with the user **without the password** — just like a real API would never return the stored credential.

##### `verifyLogin(id, password)`

```
Simulates: POST /auth/login  (conceptually)
```

- Looks up the user by exact `id` match.
- Rejects with status 404 if no user has that ID (`"User not found. Please check your ID."`).
- Rejects with status 401 if the password does not match (`"Incorrect password. Please try again."`).
- Resolves with the user without the password field.
- Specific error messages are surfaced directly in the login form's alert box — the login script passes `err.message` straight to `showAlert()`.

##### `updateUserPassword(id, oldPassword, newPassword)`

```
Simulates: PATCH /users/:id/password  (conceptually)
```

- Finds the user by ID; rejects 404 if not found.
- Verifies `oldPassword` matches the stored value; rejects 401 if not.
- Mutates `users[idx].password` in-place, saves the array, and resolves with a success message.
- Called by `change-password.js`.

---

### 4.3 `session.js` — Session Manager

**Purpose:** A lightweight wrapper around a single localStorage key (`lyfter_session`) that stores the currently logged-in user's data as a JSON string. It is separate from the user database (`lyfter_users`) so that auth checks are O(1) key lookups rather than array scans.

```js
const Session = (() => { ... return { save, get, clear, isLoggedIn }; })();
```

Again, an IIFE module — the storage key is private.

| Method                 | What it does                                                                                          |
| ---------------------- | ----------------------------------------------------------------------------------------------------- |
| `Session.save(user)`   | Serialises the user object (no password — the API already stripped it) and writes to `lyfter_session` |
| `Session.get()`        | Returns the parsed user object, or `null` if not logged in                                            |
| `Session.clear()`      | Removes `lyfter_session` from localStorage (logout)                                                   |
| `Session.isLoggedIn()` | Returns `true` if `Session.get()` is not `null` — used by auth guards                                 |

**Why localStorage instead of a cookie or sessionStorage?**
Using `localStorage` means the session persists across browser tab closes and restarts (unlike `sessionStorage`). This matches requirement 5 of the exercise ("session must survive reloads and browser close/reopen"). A real app would use an HttpOnly cookie instead, but that requires a server.

---

### 4.4 `register.html` + `register.js` — Registration Page

#### `register.html`

**Structure:**

```
<nav class="navbar">           ← "Lyfter" brand + Register(active) / Login links
<div class="page">
  <div class="card">
    <div id="alert">           ← Global success/error banner (hidden by default)
    <form id="registerForm">
      name / email / phone / age / password / confirmPassword
      ↓ Each field:
        <input id="fieldName" />
        <span class="field-error" id="fieldName-error"></span>
    </form>
  </div>
</div>
<script src="db.js"></script>
<script src="session.js"></script>
<script src="register.js"></script>
```

- `novalidate` on the `<form>` disables the browser's built-in HTML5 validation so the custom JS validation runs instead — giving full control over error messages and styling.
- Each input has a paired `<span class="field-error" id="fieldName-error">` immediately below it. The span always exists in the DOM (preventing layout shifts); JS just populates its `textContent`.
- Scripts are at the bottom of `<body>` so the DOM is fully parsed before any JS tries to query elements.

#### `register.js`

Wrapped in an IIFE so its local variables (`form`, `alertBox`, `submitBtn`, etc.) do not leak to `window`.

**Step-by-step execution:**

1. **Auth guard (immediate)**

   ```js
   if (Session.isLoggedIn()) {
     window.location.href = "profile.html";
     return;
   }
   ```

   Runs synchronously before anything else. If a session already exists, the user is bounced to the profile page immediately — they should not be able to re-register while logged in.

2. **Element references**
   Queries `registerForm`, `alert`, and `submitBtn` once and stores them in constants. `FIELDS` is an array of all field IDs used to loop over error clearing.

3. **`showAlert(message, type)` / `hideAlert()`**
   Sets the class on `#alert` to `alert alert-error` or `alert alert-success`, populates `textContent`, and calls `scrollIntoView` so it is always visible even if the user has scrolled down.

4. **`setFieldError(fieldId, message)` / `clearAllErrors()`**
   Adds or removes the `.error` class from an input and sets the text of its paired `<span>`. Called per-field during validation. `clearAllErrors()` loops over all `FIELDS` and also hides the global alert — called at the start of every submit attempt to reset state.

5. **`setLoading(loading)`**
   Disables the submit button and swaps its inner HTML to include a CSS spinner while `loading === true`. Prevents double-submission and gives visual feedback during the 400 ms simulated API call.

6. **`showSuccessModal(userId)`**
   Builds and injects a modal overlay directly into `<body>` using `createElement` and `innerHTML`. The modal shows the new User ID in a copyable box with a "Copy ID" button.
   - **Copy logic:** Uses `navigator.clipboard.writeText()` (Clipboard API). Falls back to `document.createRange()` + `window.getSelection()` for `file://` origins (where the Clipboard API may be blocked).
   - **Continue button:** Redirects to `profile.html`. There is no way to dismiss the modal without continuing, ensuring the user sees their ID before moving on.
   - The modal replaces the native `alert()` call from the original exercise draft — modals allow text selection and copy, native alerts do not.

7. **`validate(fields)`**
   Client-side validation runs synchronously before the API call:
   - `name`: must not be empty.
   - `email`: must match `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` — a basic but pragmatic regex that catches the most common typos.
   - `phone`: must not be empty.
   - `age`: must parse to an integer between 1 and 120.
   - `password`: must not be empty and must be ≥ 6 characters.
   - `confirmPassword`: must match `password`.
     All errors are accumulated (every field is checked regardless of prior failures) so the user sees all problems at once, not one at a time.

8. **`form.addEventListener('submit', async fn)`**
   The submit handler:

   ```
   e.preventDefault()          ← stop browser from navigating
   clearAllErrors()            ← reset all error state
   read field values           ← trim strings where appropriate
   validate(fields)            ← if invalid, return early (errors already shown)
   setLoading(true)            ← disable button + show spinner
   build newObject             ← { name, password, data: { email, phone, age } }
   await API.postNewObject()   ← 400 ms Promise
   Session.save(createdUser)   ← persist session
   setLoading(false)           ← re-enable button
   showSuccessModal(id)        ← show modal with User ID
   ```

   On error:

   ```
   setLoading(false)
   showAlert(err.message, 'error')   ← e.g. "This email is already registered."
   ```

9. **Dead code at the bottom of the file**
   Lines 233 onward (`const userInstance = axios.create(...)` etc.) are a leftover draft from the original axios-based version. They are never executed because the IIFE at the top of the file contains the real logic. They serve as historical context/notes linking back to `axios_exercise2.js`.

---

### 4.5 `login.html` + `login.js` — Login Page

#### `login.html`

**Structure:**

```
<nav>   ← Register / Login(active)
<form id="loginForm">
  userId (text input)
  password (password input)
  <div class="checkbox-group"> rememberMe checkbox
</form>
<div class="divider"> or </div>
<a href="register.html" class="btn btn-secondary">Create an account</a>
<p> Forgot your password? → change-password.html </p>
```

Key difference from register: includes a **"Remember my User ID"** checkbox and a link to the change-password page for users who forgot their password.

#### `login.js`

**Step-by-step execution:**

1. **Auth guard** — same pattern as register: if already logged in, redirect to profile.

2. **Remember Me pre-fill**

   ```js
   const savedId = localStorage.getItem(REMEMBER_KEY);
   if (savedId) {
     userIdInput.value = savedId;
     rememberCheckbox.checked = true;
   }
   ```

   On page load, checks `lyfter_remember_id` in localStorage. If it exists, pre-populates the User ID field and checks the checkbox — a UX convenience for returning users.

3. **Helpers** — same pattern as register: `showAlert`, `hideAlert`, `setFieldError`, `clearAllErrors`, `setLoading`.

4. **`validate(userId, password)`**
   Simpler than register — only checks that both fields are non-empty. The real validation (ID existence, password correctness) is delegated to `API.verifyLogin()`.

5. **Submit handler:**

   ```
   e.preventDefault()
   clearAllErrors()
   validate() — return early if blank
   setLoading(true)
   await API.verifyLogin(userId, password)   ← 400 ms Promise
   ```

   On success:

   ```
   if rememberMe.checked → localStorage.setItem(REMEMBER_KEY, userId)
   else                  → localStorage.removeItem(REMEMBER_KEY)
   Session.save(user)
   window.location.href = 'profile.html'
   ```

   On error:

   ```
   setLoading(false)
   showAlert(err.message, 'error')
   // err.message is one of: "User not found..." or "Incorrect password..."
   ```

   The Remember Me decision happens **after** a successful login — there is no point saving the ID if the credentials are wrong.

---

### 4.6 `profile.html` + `profile.js` — Profile Page

#### `profile.html`

Minimal markup — intentionally light because `profile.js` renders everything dynamically:

```html
<div class="card card-wide" id="profileCard">
  <div>Loading profile…</div>
  ← placeholder replaced by JS immediately
</div>
```

The "Loading profile…" text is a placeholder that disappears the moment `render()` runs (synchronously after the auth guard passes). It would only be visible if JS were somehow delayed.

Navbar has a `<button id="navLogoutBtn">` rather than a link, because logout is an action, not navigation.

#### `profile.js`

**Step-by-step execution:**

1. **Auth guard (reverse)**

   ```js
   if (!Session.isLoggedIn()) {
     window.location.href = "login.html";
     return;
   }
   ```

   Profile is the only page that redirects **away** if no session exists (all other pages redirect away if a session **does** exist).

2. **Read session**

   ```js
   const user = Session.get();
   ```

   All subsequent rendering uses this object — no DB call needed. The session already contains the safe user data (no password).

3. **`getInitials(name)`**
   Splits the name on spaces, takes the first letter of each word, limits to 2 initials, uppercases — e.g. `"John Doe"` → `"JD"`. Used to render the avatar circle without images.

4. **`formatDate(isoString)`**
   Converts the `createdAt` ISO string to a human-readable date like `"April 27, 2026"` using `toLocaleDateString('en-US', { year, month, day })`.

5. **`logout()`**
   Calls `Session.clear()` and redirects to `login.html`. Referenced by both the navbar button and the card button so the same function handles both.

6. **`render()`**
   Replaces `profileCard.innerHTML` with:
   - **Profile header:** avatar circle (initials), full name, User ID in monospace, "Member since" date.
   - **Data grid:** 2-column CSS Grid with four info cards — Email, Phone, Age, User ID.
   - **Action buttons:** "Change Password" link and "Log Out" danger button.

   After injecting the HTML, immediately re-queries `#cardLogoutBtn` and attaches the logout handler. This is necessary because the element did not exist in the DOM before `innerHTML` ran.

7. **Init:** attaches logout to the navbar button, then calls `render()`.

---

### 4.7 `change-password.html` + `change-password.js` — Change Password Page

#### `change-password.html`

```
<nav>
  <div id="navLinks">  ← populated dynamically by change-password.js
</nav>
<form id="changePasswordForm">
  userId / oldPassword / newPassword / confirmPassword
</form>
<a href="login.html">← Back to Login</a>
```

The `#navLinks` div is empty in the HTML and filled by JS based on whether the user is logged in. This is the only page that adapts its navigation dynamically (profile and login have static navbars; this page is reachable both logged-in and logged-out).

#### `change-password.js`

**This page works in two modes:**

| Mode           | Who uses it                                        | What changes                                              |
| -------------- | -------------------------------------------------- | --------------------------------------------------------- |
| **Logged-in**  | User arriving from the profile page                | User ID pre-filled, navbar shows "My Profile" + "Log Out" |
| **Logged-out** | User arriving from the login page's "Forgot?" link | User ID blank, navbar shows "Register" + "Login"          |

**Step-by-step execution:**

1. **Session check and navbar population (runs immediately)**

   ```js
   const session = Session.get(); // null if not logged in
   ```

   - If `session` exists: fills `#userId` with `session.id`, builds navbar with "My Profile" link and "Log Out" button, attaches logout handler.
   - If no session: builds navbar with "Register" and "Login" links.

   Note: there is **no auth guard redirect** here. This page is intentionally accessible without a session so logged-out users can reset their forgotten password.

2. **Helpers** — same pattern: `showAlert`, `hideAlert`, `setFieldError`, `clearAllErrors`, `setLoading`.

3. **`validate(fields)`**
   - `userId`: must not be empty.
   - `oldPassword`: must not be empty.
   - `newPassword`: must not be empty and must be ≥ 6 characters.
   - `confirmPassword`: must match `newPassword`.

4. **Submit handler:**

   ```
   e.preventDefault()
   clearAllErrors()
   validate() — return early if invalid
   setLoading(true)
   await API.updateUserPassword(userId, oldPassword, newPassword)
   ```

   On success:

   ```
   showAlert('Password updated successfully!', 'success')
   form.reset()
   if (session && session.id === fields.userId) {
     // User just changed their OWN password
     Session.clear()
     showAlert('Password updated! Redirecting to login…', 'success')
     setTimeout(() => window.location.href = 'login.html', 2000)
   } else {
     // Admin-like use case OR logged-out user — stay on page
     if (session) userIdInput.value = session.id  // re-fill ID for convenience
   }
   ```

   **Why clear the session on own-password change?**
   The stored session object contains no password hash — but the session's existence represents "I proved my identity with the old credentials." After a password change, the old credentials are invalid. Clearing the session forces re-authentication with the new password, which is the secure behavior.

   On error:

   ```
   setLoading(false)
   showAlert(err.message, 'error')  // "User not found" or "Current password is incorrect"
   ```

---

## 5. Data Shapes

### User object in `lyfter_users` (DB, includes password)

```json
{
  "id": "USR-LX2A4B-K9F3J",
  "name": "John Doe",
  "password": "secret123",
  "data": {
    "email": "john@example.com",
    "phone": "+1 555 000 0000",
    "age": 25
  },
  "createdAt": "2026-04-27T14:32:00.000Z"
}
```

### User object returned by API (no password)

```json
{
  "id": "USR-LX2A4B-K9F3J",
  "name": "John Doe",
  "data": {
    "email": "john@example.com",
    "phone": "+1 555 000 0000",
    "age": 25
  },
  "createdAt": "2026-04-27T14:32:00.000Z"
}
```

### Session object in `lyfter_session`

Same as the API-returned object (no password). Written by `Session.save(user)` after register or login.

---

## 6. localStorage Keys Reference

| Key                  | Written by                                      | Read by                                              | Purpose                                          |
| -------------------- | ----------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------ |
| `lyfter_users`       | `db.js` (`postNewObject`, `updateUserPassword`) | `db.js` (all methods)                                | Master user database array                       |
| `lyfter_session`     | `session.js` (`save`)                           | `session.js` (`get`, `isLoggedIn`), all page scripts | Currently logged-in user                         |
| `lyfter_remember_id` | `login.js`                                      | `login.js` (on page load)                            | Remembered User ID for the "Remember Me" feature |

---

## 7. Security & Design Decisions

| Decision                                            | Reason                                                                                                                                                                               |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Passwords stored in plain text in localStorage      | This is a **learning exercise only**. In production, passwords must be hashed (bcrypt/Argon2) server-side and never stored client-side.                                              |
| `password` field stripped from every API response   | Mirrors real API behavior — the calling code never receives the credential back, even though the storage is local.                                                                   |
| IIFE module pattern for `API` and `Session`         | Prevents accidental global variable collisions and makes the internal state (storage keys, helpers) private.                                                                         |
| `novalidate` on all forms                           | Delegates all validation to JS for consistent cross-browser UX and styling control.                                                                                                  |
| Error messages from `err.message` surfaced directly | The `db.js` errors include user-friendly messages designed for display. No need for a secondary mapping layer.                                                                       |
| Session cleared on own-password change              | Security principle: changing a credential should invalidate existing sessions.                                                                                                       |
| `db.js` + `session.js` loaded before page scripts   | Ensures the `API` and `Session` globals exist before any page script tries to call them. Script order in HTML is the dependency injection mechanism here (no bundler/module system). |
| `navigator.clipboard` with `createRange` fallback   | `file://` protocol blocks the Clipboard API in some browsers; the selection fallback ensures copy-ID still works when opening HTML files directly.                                   |
| 400 ms simulated delay in all API calls             | Makes the UI behave realistically — spinners are visible, the button disabled state is testable — even without a network.                                                            |
