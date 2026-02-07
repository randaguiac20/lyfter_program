# Semana 8 - Fruit Products REST API with Redis Caching

A Flask-based REST API for managing fruit products with PostgreSQL database, JWT authentication, HTTPS, and Redis caching.

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Environment Setup](#environment-setup)
- [Docker Commands](#docker-commands)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
- [Application Workflow](#application-workflow)
- [Redis Caching](#redis-caching)

---

## 📦 Prerequisites

- Python 3.9+
- Docker & Docker Compose
- Redis Cloud account (or local Redis instance)
- SSL certificates (for HTTPS)

---

## 📁 Project Structure

```
semana8/
├── ejercicio1/
│   ├── main.py                 # Application entry point
│   ├── docker-compose.yml      # PostgreSQL container config
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│   ├── certs/                  # SSL certificates
│   ├── secrets/                # JWT tokens and keys
│   ├── modules/
│   │   ├── config.py           # App configuration
│   │   ├── db_manager.py       # Database operations (SQLAlchemy)
│   │   ├── jwt_manager.py      # JWT authentication
│   │   ├── cache_manager.py    # Redis cache operations
│   │   ├── cache_config.py     # Flask-Caching setup
│   │   ├── https_config.py     # SSL context configuration
│   │   ├── models.py           # SQLAlchemy ORM models
│   │   └── secret_keys.py      # Password hashing utilities
│   └── repositories/
│       ├── repository.py       # Base repository class
│       ├── user_repository.py
│       ├── registration_repository.py
│       ├── login_repository.py
│       ├── product_repository.py
│       ├── address_repository.py
│       ├── receipt_repository.py
│       ├── shoppping_cart_repository.py
│       ├── shoppping_cart_product_repository.py
│       └── buy_fruits_repository.py
└── test_redis.py               # Redis connection testing
```

---

## 🚀 Quick Start

### 1. Activate Python Virtual Environment

```bash
# Activate the v39_lyfter virtual environment
source /Users/Randall_Aguilar/projects/personal/v39_lyfter/bin/activate

# Verify activation
which python
# Should output: /Users/Randall_Aguilar/projects/personal/v39_lyfter/bin/python
```

### 2. Navigate to Project Directory

```bash
cd /Users/Randall_Aguilar/projects/personal/git/lyfter_program/module2/semana8/ejercicio1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start PostgreSQL with Docker

```bash
docker-compose up -d
```

### 5. Run the Application

```bash
python main.py
```

The API will be available at: `https://localhost:5001`

---

## ⚙️ Environment Setup

### Environment Variables (.env)

Create or update the `.env` file in `ejercicio1/`:

```env
# Database Configuration
DB_NAME=lyfter_8_week
DB_USERNAME=randall_aguilar
DB_PASSWORD=lyfter_password
DB_HOST=localhost
DB_PORT=5452
SCHEMA=lyfter_week_8

# Redis Configuration
REDIS_HOST=redis-14470.c283.us-east-1-4.ec2.cloud.redislabs.com
REDIS_PORT=14470
REDIS_PASSWORD=your_redis_password

# Admin Configuration
DEFAULT_ADMIN=your_password

# Secrets Path
FILE_PATH=/path/to/secrets
```

---

## 🐳 Docker Commands

### Start PostgreSQL Container

```bash
# Navigate to ejercicio1 directory
cd /Users/Randall_Aguilar/projects/personal/git/lyfter_program/module2/semana8/ejercicio1

# Start container in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Check container status
docker-compose ps
```

### Stop PostgreSQL Container

```bash
# Stop container (keeps data)
docker-compose stop

# Stop and remove container (keeps volume data)
docker-compose down

# Stop, remove container AND delete all data
docker-compose down -v
```

### Database Access

```bash
# Connect to PostgreSQL inside container
docker exec -it lyfter_postgres_week_8 psql -U randall_aguilar -d lyfter_8_week

# Or connect from host machine
psql -h localhost -p 5452 -U randall_aguilar -d lyfter_8_week
```

---

## 🏃 Running the Application

### Step-by-Step Guide

#### Step 1: Activate Virtual Environment
```bash
source /Users/Randall_Aguilar/projects/personal/v39_lyfter/bin/activate
```

#### Step 2: Start Docker Services
```bash
cd /Users/Randall_Aguilar/projects/personal/git/lyfter_program/module2/semana8/ejercicio1
docker-compose up -d
```

#### Step 3: Wait for PostgreSQL to be Ready
```bash
# Check if PostgreSQL is healthy
docker-compose ps
# STATUS should show "healthy"
```

#### Step 4: Run the Flask Application
```bash
python main.py
```

#### Expected Output:
```
 * Serving Flask app 'main'
 * Debug mode: on
 * Running on https://localhost:5001
```

#### Step 5: Test the API
```bash
# Test login endpoint
curl -k -X POST https://localhost:5001/fruit_products/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@administrator.com", "password": "Just0n3Adm1inP455word"}'
```

---

## 🔌 API Endpoints

Base URL: `https://localhost:5001/fruit_products`

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/login` | User login | No |
| GET | `/me` | Get current user | Yes |
| POST | `/refresh-token` | Refresh JWT token | Yes |

### User Registration (Admin Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/register` | List all registrations |
| POST | `/register` | Create new registration |
| GET | `/register/<id>` | Get registration by ID |
| PUT | `/register/<id>` | Update registration |
| DELETE | `/register/<id>` | Delete registration |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users` | List all users |
| POST | `/users` | Create new user |
| GET | `/users/<id>` | Get user by ID |
| PUT | `/users/<id>` | Update user |
| DELETE | `/users/<id>` | Delete user |

### Products (Fruits)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | List all products |
| POST | `/products` | Create new product |
| GET | `/products/<id>` | Get product by ID |
| PUT | `/products/<id>` | Update product |
| DELETE | `/products/<id>` | Delete product |

### Other Endpoints

- `/addresses` - User addresses management
- `/shopping_carts` - Shopping cart management
- `/shopping_cart_products` - Cart items management
- `/receipts` - Purchase receipts
- `/buy-fruits` - Purchase transactions

---

## 🔄 Application Workflow

### Architecture Overview

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌────────────┐
│   Client    │────▶│  Flask API  │────▶│    Redis    │────▶│ PostgreSQL │
│  (Postman)  │     │  (HTTPS)    │     │   (Cache)   │     │   (Data)   │
└─────────────┘     └─────────────┘     └─────────────┘     └────────────┘
```

### Request Flow

```
1. Client sends HTTPS request
         │
         ▼
2. Flask receives request
         │
         ▼
3. JWT Authentication (if required)
    ├── Invalid token → 401 Unauthorized
    └── Valid token → Continue
         │
         ▼
4. Check Redis Cache (for GET requests)
    ├── Cache HIT → Return cached data
    └── Cache MISS → Query PostgreSQL
         │
         ▼
5. Process with Repository
         │
         ▼
6. Return JSON Response
```

### Authentication Flow

```
┌──────────────────────────────────────────────────────────────┐
│                      LOGIN FLOW                              │
└──────────────────────────────────────────────────────────────┘

1. POST /login with email + password
         │
         ▼
2. Verify credentials against PostgreSQL
    ├── Invalid → 401 Unauthorized
    └── Valid → Continue
         │
         ▼
3. Generate JWT Token
         │
         ▼
4. Return token to client
         │
         ▼
5. Client stores token for future requests
         │
         ▼
6. Include token in header: Authorization: Bearer <token>
```

### Data Flow Example (Create User)

```
POST /fruit_products/users
Header: Authorization: Bearer <jwt_token>
Body: {"first_name": "John", "last_name": "Doe", ...}

         │
         ▼
    ┌────────────┐
    │ Validate   │
    │ JWT Token  │
    └────────────┘
         │
         ▼
    ┌────────────┐
    │ Validate   │
    │ Request    │
    └────────────┘
         │
         ▼
    ┌────────────┐
    │ Insert to  │
    │ PostgreSQL │
    └────────────┘
         │
         ▼
    ┌────────────┐
    │ Invalidate │
    │ Redis Cache│
    └────────────┘
         │
         ▼
    Return: {"id": 1, "created_at": "..."}
```

---

## 🔴 Redis Caching

### How Caching Works

```
GET Request Flow:
─────────────────
1. Generate cache key (e.g., "products:42")
2. Check if key exists in Redis
   ├── YES → Return cached JSON (fast!)
   └── NO  → Query PostgreSQL
           → Store result in Redis (with TTL)
           → Return data

Write Request Flow (POST/PUT/DELETE):
─────────────────────────────────────
1. Perform database operation
2. Invalidate related cache keys
3. Return response
```

### Cache Key Patterns

| Resource | Single Item | List |
|----------|-------------|------|
| Products | `products:{id}` | `products:list:*` |
| Users | `users:{id}` | `users:list:*` |

### Testing Redis Connection

```bash
cd /Users/Randall_Aguilar/projects/personal/git/lyfter_program/module2/semana8
python test_redis.py
```

---

## 🧪 Testing with cURL

### Login
```bash
curl -k -X POST https://localhost:5001/fruit_products/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@administrator.com", "password": "your_password"}'
```

### Get Products (with token)
```bash
curl -k -X GET https://localhost:5001/fruit_products/products \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Create Product
```bash
curl -k -X POST https://localhost:5001/fruit_products/products \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"name": "Apple", "price": 1.50, "quantity": 100}'
```

---

## 🛠️ Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| `Connection refused` on port 5452 | Run `docker-compose up -d` |
| `ModuleNotFoundError` | Activate venv: `source ~/projects/personal/v39_lyfter/bin/activate` |
| SSL certificate error | Use `-k` flag with curl or generate valid certs |
| Redis connection error | Check REDIS_HOST, REDIS_PORT, REDIS_PASSWORD in .env |

### Useful Commands

```bash
# Check if PostgreSQL container is running
docker ps | grep lyfter_postgres

# View application logs
docker-compose logs -f

# Reset database (delete all data)
docker-compose down -v && docker-compose up -d
```

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Redis Documentation](https://redis.io/docs/)
- [JWT Authentication](https://jwt.io/)
