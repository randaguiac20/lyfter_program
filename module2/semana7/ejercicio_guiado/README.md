# User Authentication Service with JWT

A Flask-based REST API microservice that provides user authentication using JWT (JSON Web Tokens) and PostgreSQL for data persistence.

## Overview

This application implements a user authentication system with three main functionalities:
- **User Registration** - Create new user accounts
- **User Login** - Authenticate existing users
- **User Profile** - Retrieve authenticated user information

All sensitive routes are protected using JWT tokens for secure authentication.

## Architecture

### Tech Stack
- **Backend Framework**: Flask (Python)
- **Database**: PostgreSQL 15 (Alpine)
- **ORM**: SQLAlchemy
- **Database Driver**: psycopg2
- **Authentication**: PyJWT (JSON Web Tokens)
- **Containerization**: Docker & Docker Compose

### Project Structure
```
ejercicio_guiado/
├── .env                    # Environment variables (database credentials)
├── config.py              # Configuration settings
├── db.py                  # Database manager and operations
├── docker-compose.yml     # Docker container configuration
├── jwt_manager.py         # JWT encoding/decoding logic
├── main.py                # Flask application and API routes
└── README.md              # This file
```

## Components

### 1. Database Manager (`db.py`)
- **Connection**: Manages PostgreSQL connection using SQLAlchemy
- **Schema Management**: Creates and manages database schema `lyfter_week_7_guiado`
- **User Table**: Stores user credentials (id, username, password)
- **Operations**:
  - `insert_user(username, password)` - Creates new user
  - `get_user(username, password)` - Authenticates user credentials
  - `get_user_by_id(id)` - Retrieves user by ID

### 2. JWT Manager (`jwt_manager.py`)
- **Secret Key**: `trespatitos`
- **Algorithm**: HS256
- **Operations**:
  - `encode(data)` - Creates JWT token from user data
  - `decode(token)` - Validates and extracts user data from token

### 3. API Endpoints (`main.py`)

#### `GET /liveness`
Health check endpoint to verify service is running.
- **Response**: `"Hello, World!"`

#### `POST /register`
Creates a new user account and returns a JWT token.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response** (200):
  ```json
  {
    "token": "jwt_token_string"
  }
  ```
- **Error Response** (400): Missing username or password

#### `POST /login`
Authenticates user and returns JWT token.
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Success Response** (200):
  ```json
  {
    "token": "jwt_token_string"
  }
  ```
- **Error Responses**:
  - 400: Missing credentials
  - 403: Invalid credentials

#### `GET /me`
Returns authenticated user information.
- **Headers**:
  ```
  Authorization: Bearer <jwt_token>
  ```
- **Success Response** (200):
  ```json
  {
    "id": 1,
    "username": "string"
  }
  ```
- **Error Responses**:
  - 403: Missing or invalid token
  - 500: Server error

## Setup and Installation

### Prerequisites
- Docker and Docker Compose installed
- Python 3.9+ with virtual environment
- PostgreSQL client (optional, for debugging)

### Step 1: Environment Configuration

The `.env` file contains database configuration:
```env
DB_NAME=lyfter_7_week_guiado
DB_USERNAME=randall_aguilar
DB_PASSWORD=lyfter_password
DB_HOST=localhost
DB_PORT=5451
SCHEMA=lyfter_week_7_guiado
```

**Note**: No quotes around values in `.env` file for Docker Compose compatibility.

### Step 2: Start PostgreSQL Database

Navigate to the project directory:
```bash
cd /Users/Randall_Aguilar/projects/personal/git/lyfter_program/module2/semana7/ejercicio_guiado
```

Start the PostgreSQL container:
```bash
docker compose up -d
```

Verify the database is running:
```bash
docker compose ps
```

Check database creation:
```bash
docker exec lyfter_postgres_week_7 psql -U randall_aguilar -l
```

### Step 3: Activate Python Virtual Environment

Activate the existing virtual environment:
```bash
source /Users/Randall_Aguilar/projects/personal/v39_lyfter/bin/activate
```

### Step 4: Install Dependencies (if needed)

The virtual environment should already have these packages:
```bash
pip install flask sqlalchemy psycopg2-binary pyjwt
```

### Step 5: Run the Application

```bash
python main.py
```

The application will start on `http://localhost:5000`

You should see output like:
```
 * Running on http://localhost:5000
 * Debug mode: on
```

## Usage Examples

### 1. Register a New User

```bash
curl -X POST http://localhost:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 2. Login

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

Response:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### 3. Get User Profile

```bash
curl -X GET http://localhost:5000/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

Response:
```json
{
  "id": 1,
  "username": "testuser"
}
```

## Database Details

### Connection String Format
```
postgresql+psycopg2://[username]:[password]@[host]:[port]/[database]
```

### Docker PostgreSQL Configuration
- **Container Name**: `lyfter_postgres_week_7`
- **Image**: `postgres:15-alpine`
- **Port Mapping**: `5451:5432` (host:container)
- **Database**: `lyfter_7_week_guiado`
- **Schema**: `lyfter_week_7_guiado`
- **Volume**: `ejercicio_guiado_postgres_data`

### Table Structure
```sql
CREATE TABLE lyfter_week_7_guiado.users (
    id SERIAL NOT NULL PRIMARY KEY,
    username VARCHAR(30),
    password VARCHAR
);
```

## Database Management

### Access PostgreSQL Shell
```bash
docker exec -it lyfter_postgres_week_7 psql -U randall_aguilar -d lyfter_7_week_guiado
```

### View Tables
```sql
\dt lyfter_week_7_guiado.*
```

### Query Users
```sql
SELECT * FROM lyfter_week_7_guiado.users;
```

### Stop Database
```bash
docker compose down
```

### Reset Database (removes all data)
```bash
docker compose down -v
docker compose up -d
```

## Important Notes

### Security Considerations ⚠️
1. **Passwords are stored in plain text** - In production, use bcrypt or similar hashing
2. **JWT secret is hardcoded** - Should be stored in environment variables
3. **No token expiration** - Tokens should have expiration times
4. **No HTTPS** - Use HTTPS in production
5. **No input validation** - Should validate username/password format

### Database Connection
The application uses `postgresql+psycopg2://` which explicitly specifies the psycopg2 driver. This ensures:
- Predictable behavior across environments
- Compatibility with the installed driver
- No automatic driver detection issues

### Docker Compose vs docker-compose
- Use `docker compose` (newer, integrated with Docker)
- `docker-compose` is the older standalone tool
- Both work, but `docker compose` is recommended

## Troubleshooting

### Database Does Not Exist Error
If you see `database "lyfter_7_week_guiado" does not exist`:
1. Check `.env` file has no quotes around values
2. Restart Docker with volume removal: `docker compose down -v && docker compose up -d`

### Schema Does Not Exist Error
If you see `schema "lyfter_week_7_guiado" does not exist`:
- The code creates the schema automatically before creating tables
- Ensure `_ensure_schema()` is called before `metadata_obj.create_all()`

### Port Already in Use
If port 5451 is busy:
1. Change the port in `docker-compose.yml` (e.g., `5452:5432`)
2. Update `.env` file: `DB_PORT=5452`
3. Restart: `docker compose down && docker compose up -d`

### Python Command Not Found
Use the virtual environment:
```bash
source /Users/Randall_Aguilar/projects/personal/v39_lyfter/bin/activate
```

## Development

### Debug Mode
The application runs with `debug=True`, which:
- Auto-reloads on code changes
- Shows detailed error messages
- Enables the debugger

### Database Echo
Set `echo=True` in `create_engine()` to see all SQL queries:
```python
self.engine = create_engine(self.db_uri, echo=True)
```

## Future Improvements

1. **Password Hashing**: Implement bcrypt for secure password storage
2. **Token Expiration**: Add expiration time to JWT tokens
3. **Refresh Tokens**: Implement refresh token mechanism
4. **Input Validation**: Add validation for username/password requirements
5. **Error Handling**: Improve error messages and logging
6. **Environment Variables**: Move JWT secret to environment variables
7. **User Update/Delete**: Add endpoints for user management
8. **Rate Limiting**: Prevent brute force attacks
9. **CORS Configuration**: Add proper CORS headers for frontend integration
10. **Unit Tests**: Add comprehensive test coverage

## License

Educational project for Lyfter Module 2, Week 7.

## Contact

Randall Aguilar - Week 7 Guided Exercise
