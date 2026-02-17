# E-Commerce Pets API

REST API for a pet shop e-commerce platform built with Flask, PostgreSQL, Redis, and JWT authentication over HTTPS.

## Prerequisites

- Python 3.10+
- Docker & Docker Compose (for PostgreSQL)
- Redis instance (cloud or local)

## Setup

### 1. Clone and enter the project

```bash
cd final_ecommerce_pets
```

### 2. Create and activate the virtual environment

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
```

### 3. Install dependencies

```bash
pip install flask sqlalchemy psycopg2-binary python-dotenv pyjwt cryptography werkzeug redis pytest
```

> **Note:** Always activate the venv before running the app or tests. All commands below assume the venv is active.

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
DB_NAME=your_database_name
DB_USERNAME=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5452
SCHEMA=e_comerce_pets_lyfter

REDIS_HOST=your_redis_host
REDIS_PORT=your_redis_port
REDIS_PASSWORD=your_redis_password

DEFAULT_ADMIN=your_admin_password

FILE_PATH=/absolute/path/to/project/secrets
```

### 5. Start PostgreSQL

```bash
docker compose up -d
```

This starts a PostgreSQL 15 container on the port defined in `DB_PORT`.

### 6. Create the secrets directory

```bash
mkdir -p secrets
```

RSA keys (`private.pem`, `public.pem`) and the admin token are generated automatically on startup.

## Running the App

```bash
source venv/bin/activate
python e_main.py
```

The server starts at `https://localhost:5001` with a self-signed SSL certificate.

On startup the app will:
1. Generate RSA key pair (in `secrets/`)
2. Generate SSL dev certificates (in `certs/`)
3. Create all database tables (drops existing ones first)
4. Create the default admin user
5. Generate a JWT token (saved to `secrets/token`)

## API Endpoints

All endpoints are prefixed with `/e_commerce_pets`.

| Resource | Methods | Auth Required |
|---|---|---|
| `/login` | POST | No |
| `/register` | GET, POST | Admin |
| `/register/<id>` | GET, PUT, DELETE | Admin |
| `/refresh-token` | POST | Any |
| `/users` | GET, POST | Admin |
| `/users/<id>` | GET, PUT, DELETE | Admin |
| `/addresses` | GET, POST | Admin |
| `/addresses/<id>` | GET, PUT, DELETE | Admin |
| `/products` | GET | Admin, Client |
| `/products` | POST | Admin |
| `/products/<id>` | GET | Admin, Client |
| `/products/<id>` | PUT, DELETE | Admin |
| `/shopping_carts` | GET, POST | Admin, Client |
| `/shopping_carts/<id>` | GET, PUT, DELETE | Admin, Client |
| `/shopping_cart_products` | GET, POST | Admin, Client |
| `/shopping_cart_products/<id>` | GET, PUT, DELETE | Admin, Client |
| `/receipts` | GET | Admin, Client |
| `/receipts` | POST | Admin |
| `/receipts/<id>` | GET | Admin, Client |
| `/receipts/<id>` | PUT, DELETE | Admin |
| `/user_contacts` | GET | Admin, Client |
| `/user_contacts` | POST | Admin |
| `/user_contacts/<id>` | GET | Admin, Client |
| `/user_contacts/<id>` | PUT, DELETE | Admin |
| `/me` | GET | Any |

### Authentication

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <your_token>
```

## Running Tests

Tests use an in-memory SQLite database and mocked Redis — no external services needed.

```bash
source venv/bin/activate

# Using the runner script (recommended)
python run_tests.py

# Or directly with pytest
TESTING=true python -m pytest test/ -v

# Run only success or failure tests
TESTING=true python -m pytest test/test_api.py::TestAPISuccess -v
TESTING=true python -m pytest test/test_api.py::TestAPIFailure -v

# Run a single test
TESTING=true python -m pytest test/test_api.py::TestAPISuccess::test_login_success -v
```

The test suite includes 10 tests (5 success + 5 failure). See `doc/TESTING_GUIDE.md` for full details on the test architecture and `doc/CODE_FIXES.md` for the infrastructure changes that enable testing.

## Project Structure

```
final_ecommerce_pets/
├── e_main.py                  # App entry point
├── docker-compose.yml         # PostgreSQL container
├── run_tests.py               # Test runner script
├── .env                       # Environment variables (not committed)
├── venv/                      # Python virtual environment (not committed)
├── modules/
│   ├── config.py              # App configuration
│   ├── db_manager.py          # SQLAlchemy database manager
│   ├── models.py              # ORM models
│   ├── jwt_manager.py         # JWT auth and @require_jwt decorator
│   ├── cache_manager.py       # Redis cache wrapper
│   ├── secret_keys.py         # RSA keys and password hashing
│   └── https_config.py        # SSL certificate setup
├── repositories/
│   ├── repository.py          # Base repository (ABC + MethodView)
│   ├── login_repository.py
│   ├── registration_repository.py
│   ├── refresh_token_repository.py
│   ├── user_repository.py
│   ├── address_repository.py
│   ├── product_repository.py
│   ├── receipt_repository.py
│   ├── shoppping_cart_repository.py
│   ├── shoppping_cart_product_repository.py
│   └── user_contact_repository.py
├── test/
│   ├── conftest.py            # Test fixtures and mocks
│   └── test_api.py            # Unit tests (5 success + 5 failure)
├── secrets/                   # RSA keys and token (auto-generated)
├── certs/                     # SSL certificates (auto-generated)
└── doc/
    ├── CACHING_STRATEGY.md    # Cache design decisions
    ├── CODE_FIXES.md          # Infrastructure fixes for testability
    └── TESTING_GUIDE.md       # Full testing setup guide
```
