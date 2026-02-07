# Fruit Products API - Week 7 Exercise

A Flask-based REST API for a fruit store management system with JWT authentication (RS256), role-based access control, and HTTPS support.

---

## 📁 Project Structure

```
ejercicio1/
├── certs/                  # SSL certificates (dev.crt, dev.key)
├── modules/
│   ├── config.py           # Database and app configuration
│   ├── db_manager.py       # Database manager (SQLAlchemy ORM)
│   ├── jwt_manager.py      # JWT authentication with RS256
│   ├── models.py           # SQLAlchemy models
│   ├── secret_keys.py      # Key generation and password hashing
│   ├── https_config.py     # SSL configuration
│   └── cache_config.py     # Flask-Caching configuration
├── repositories/           # API endpoints (MethodView pattern)
│   ├── login_repository.py
│   ├── registration_repository.py
│   ├── user_repository.py
│   ├── address_repository.py
│   ├── product_repository.py
│   ├── shoppping_cart_repository.py
│   ├── receipt_repository.py
│   ├── shoppping_cart_product_repository.py
│   └── buy_fruits_repository.py    # PUBLIC API
├── secrets/                # Generated keys and tokens
│   ├── private.pem
│   ├── public.pem
│   └── token
├── .env                    # Environment variables
├── docker-compose.yml      # PostgreSQL container
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
└── INSTRUCTIONS.md         # Exercise instructions
```

---

## 🐳 Docker Setup

### Prerequisites
- Docker and Docker Compose installed
- Python 3.9+

### 1. Start PostgreSQL Database

```bash
cd module2/semana7/ejercicio1

# Start the PostgreSQL container
docker-compose up -d

# Verify container is running
docker ps

# Check container logs if needed
docker logs lyfter_postgres_week_7
```

### 2. Stop Database

```bash
docker-compose down

# To remove volumes (WARNING: deletes all data)
docker-compose down -v
```

### Environment Variables (.env)

```env
DB_NAME=lyfter_7_week
DB_USERNAME=randall_aguilar
DB_PASSWORD=lyfter_password
DB_HOST=localhost
DB_PORT=5452
SCHEMA=lyfter_week_7
```

---

## 🚀 Running the Application

### 1. Install Dependencies

```bash
cd module2/semana7/ejercicio1

# Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Start the API Server

```bash
python main.py
```

The server will start at: **https://localhost:5001**

> ⚠️ **Note:** The application uses self-signed SSL certificates. Your browser/client may show a security warning - this is expected for development.

---

## 🔐 Authentication & Authorization

### Roles
| Role | Access |
|------|--------|
| **administrator** | Full access to all endpoints |
| **client** | Access to: login, me, register, buy-fruits |

### Admin User (Auto-Created)

An admin user is **automatically created** when the application starts:

| Field | Value |
|-------|-------|
| Email | `admin@administrator.com` |
| Password | See `modules/config.py` → `DEFAULT_ADMIN` variable |

> 📄 **Password Location:** The admin password is defined in [`modules/config.py`](ejercicio1/modules/config.py) as `DEFAULT_ADMIN = "Just0n3Adm1inP455word"`

---

## 🌐 API Endpoints

### Private API Endpoints (Admin Only)
These endpoints are for internal management and require **administrator** role:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/POST | `/fruit_products/register` | Manage user registrations |
| GET/PUT/DELETE | `/fruit_products/register/<id>` | Single registration operations |
| GET/POST | `/fruit_products/users` | Manage users |
| GET/PUT/DELETE | `/fruit_products/users/<id>` | Single user operations |
| GET/POST | `/fruit_products/addresses` | Manage addresses |
| GET/PUT/DELETE | `/fruit_products/addresses/<id>` | Single address operations |
| GET/POST | `/fruit_products/products` | Manage products |
| GET/PUT/DELETE | `/fruit_products/products/<id>` | Single product operations |
| GET/POST | `/fruit_products/shopping_carts` | Manage shopping carts |
| GET/POST | `/fruit_products/receipts` | Manage receipts |
| GET/POST | `/fruit_products/shopping_cart_products` | Manage cart products |

### Public API Endpoint (Client Access)
This endpoint simulates a **frontend/customer-facing** purchase flow:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/fruit_products/login` | Authenticate user |
| GET | `/fruit_products/me` | Get current user info |
| GET/POST | `/fruit_products/buy-fruits` | **Purchase fruits** |

---

## 📋 API Call Sequence (Step-by-Step Setup)

To properly set up and test the system, follow this **exact sequence**:

### Step 1: Login (Get JWT Token)

**Endpoint:** `POST https://localhost:5001/fruit_products/login`

Use the auto-created admin account to get a JWT token:

```json
{
    "email": "admin@administrator.com",
    "password": "Just0n3Adm1inP455word"
}
```

**Response:**
```json
{
    "email": "admin@administrator.com",
    "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

> 💡 **Save this token!** You'll need it for all subsequent requests in the `Authorization` header as: `Bearer <token>`

---

### Step 2: Register a Client User

**Endpoint:** `POST https://localhost:5001/fruit_products/register`

**Headers:**
```
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**Body:**
```json
{
    "email": "client@example.com",
    "password": "MySecurePassword123",
    "role": "client"
}
```

**Response:**
```json
{
    "id": 2,
    "created_at": "2026-01-20 20:30:00",
    "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### Step 3: Create an Address

**Endpoint:** `POST https://localhost:5001/fruit_products/addresses`

**Headers:**
```
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**Body:**
```json
{
    "street": "123 Main Street",
    "city": "San Jose",
    "state": "San Jose",
    "postal_code": "10101",
    "country": "Costa Rica"
}
```

**Response:**
```json
{
    "id": 1,
    "postal_code": "10101",
    "country": "Costa Rica",
    "state": "San Jose",
    "created_at": "2026-01-20 20:31:00"
}
```

---

### Step 4: Create a User Profile

**Endpoint:** `POST https://localhost:5001/fruit_products/users`

**Headers:**
```
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**Body:**
```json
{
    "registration_id": 2,
    "first_name": "John",
    "last_name": "Doe",
    "telephone": "88887777",
    "address_id": 1
}
```

**Response:**
```json
{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "created_at": "2026-01-20 20:32:00"
}
```

---

### Step 5: Add Products to Inventory

**Endpoint:** `POST https://localhost:5001/fruit_products/products`

**Headers:**
```
Authorization: Bearer <admin_token>
Content-Type: application/json
```

**Body (Array of products):**
```json
[
    {
        "name": "Apple",
        "description": "Fresh red apples from local farm",
        "price": 150,
        "size": "large",
        "quantity": 100
    },
    {
        "name": "Apple",
        "description": "Fresh red apples - medium size",
        "price": 100,
        "size": "medium",
        "quantity": 150
    },
    {
        "name": "Banana",
        "description": "Organic bananas",
        "price": 75,
        "size": "medium",
        "quantity": 200
    },
    {
        "name": "Orange",
        "description": "Sweet Valencia oranges",
        "price": 120,
        "size": "large",
        "quantity": 80
    },
    {
        "name": "Mango",
        "description": "Tropical mangoes",
        "price": 200,
        "size": "large",
        "quantity": 50
    }
]
```

**Response:**
```json
[
    {
        "id": 1,
        "name": "Apple",
        "description": "Fresh red apples from local farm",
        "price": 150,
        "size": "large",
        "quantity": 100,
        "created_at": "2026-01-20 20:33:00",
        "updated_at": null
    },
    ...
]
```

---

### Step 6: Buy Fruits (Public API - Client Access)

**Endpoint:** `POST https://localhost:5001/fruit_products/buy-fruits`

**Headers:**
```
Authorization: Bearer <client_token>
Content-Type: application/json
```

> 💡 **Note:** Use the **client's token** (from Step 2 response) for this request, not the admin token.

**Body (Array of items to purchase):**
```json
[
    {
        "name": "Apple",
        "size": "large",
        "quantity": 2
    },
    {
        "name": "Banana",
        "size": "medium",
        "quantity": 5
    },
    {
        "name": "Mango",
        "size": "large",
        "quantity": 1
    }
]
```

**Response:**
```json
{
    "cart": {
        "id": 1,
        "user_id": 1,
        "status": "active",
        "purchase_date": "2026-01-20 20:35:00",
        "created_at": "2026-01-20 20:35:00"
    },
    "cart_products": [
        {
            "id": 1,
            "cart_id": 1,
            "product_id": 1,
            "quantity": 2,
            "checkout": false,
            "created_at": "2026-01-20 20:35:00"
        },
        {
            "id": 2,
            "cart_id": 1,
            "product_id": 3,
            "quantity": 5,
            "checkout": false,
            "created_at": "2026-01-20 20:35:00"
        },
        {
            "id": 3,
            "cart_id": 1,
            "product_id": 5,
            "quantity": 1,
            "checkout": false,
            "created_at": "2026-01-20 20:35:00"
        }
    ],
    "receipt": {
        "id": 1,
        "cart_id": 1,
        "payment_method": "cash",
        "total_amount": 875,
        "created_at": "2026-01-20 20:35:00"
    }
}
```

**Total Calculation:**
- Apple (large): 150 × 2 = 300
- Banana (medium): 75 × 5 = 375
- Mango (large): 200 × 1 = 200
- **Total: 875**

---

## 📊 Database Schema

The application uses the following tables:

| Table | Description |
|-------|-------------|
| `user_registrations` | Authentication credentials (email, password, role) |
| `users` | User profiles (name, telephone, address) |
| `addresses` | User addresses |
| `products` | Product inventory |
| `shopping_carts` | Shopping cart with status |
| `cart_products` | Products in each cart |
| `receipts` | Purchase receipts |
| `user_contacts` | User contact information (extra feature) |

---

## 🧪 Testing with cURL

### Login
```bash
curl -k -X POST https://localhost:5001/fruit_products/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@administrator.com", "password": "Just0n3Adm1inP455word"}'
```

### Get Products
```bash
curl -k -X GET https://localhost:5001/fruit_products/products \
  -H "Authorization: Bearer <your_token>"
```

### Buy Fruits
```bash
curl -k -X POST https://localhost:5001/fruit_products/buy-fruits \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <client_token>" \
  -d '[{"name": "Apple", "size": "large", "quantity": 2}]'
```

> 💡 The `-k` flag is used to bypass SSL certificate verification for self-signed certificates.

---

## 📝 Notes

- All endpoints use **HTTPS** with self-signed certificates
- JWT tokens use **RS256** algorithm (asymmetric)
- Tokens expire in **15 minutes** (refresh token endpoint available)
- Database tables are **recreated** on each application start (development mode)
- Valid product sizes: `"large"`, `"medium"`, `"small"`
