# Fruit Products API - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Base URL](#base-url)
3. [Authentication](#authentication)
4. [Public Endpoints](#public-endpoints)
5. [Private Endpoints (Admin Only)](#private-endpoints-admin-only)
6. [Private Endpoints (Admin & Client)](#private-endpoints-admin--client)
7. [Test Datasets](#test-datasets)
8. [Testing Plan](#testing-plan)

---

## Overview

The Fruit Products API is a RESTful service for managing a fruit store. It provides endpoints for user management, product inventory, shopping carts, and purchase transactions.

**Technology Stack:**
- Flask 2.x with MethodView pattern
- PostgreSQL 15 database
- SQLAlchemy ORM
- JWT RS256 authentication
- HTTPS with self-signed certificates

---

## Base URL

```
https://localhost:5001/fruit_products
```

> **Note:** Use `-k` flag with curl to skip SSL certificate verification for development.

---

## Authentication

### Token Types
- **Access Token**: Short-lived JWT token for API access
- **Refresh Token**: Used to obtain new access tokens

### Roles
| Role | Description |
|------|-------------|
| `administrator` | Full access to all endpoints |
| `client` | Access to public endpoints and buy-fruits |

### Headers
All protected endpoints require:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

---

## Public Endpoints

### 1. Login
**POST** `/fruit_products/login`

Authenticate user and receive JWT token.

**Access:** Public (no authentication required)

**Request Body:**
```json
{
    "email": "admin@administrator.com",
    "password": "Just0n3Adm1inP455word"
}
```

**Success Response (200):**
```json
{
    "email": "admin@administrator.com",
    "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "created_at": "2026-01-20 10:30:00.123456+00:00"
}
```

**Error Responses:**
- `404`: User not found
- `403`: Invalid password

**curl Example:**
```bash
curl -k -X POST https://localhost:5001/fruit_products/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@administrator.com", "password": "Just0n3Adm1inP455word"}'
```

---

### 2. Refresh Token
**POST** `/fruit_products/refresh-token`

Generate new access and refresh tokens.

**Access:** Requires valid JWT (administrator or client)

**Headers:**
```
Authorization: Bearer <current_token>
```

**Success Response (200):**
```json
{
    "email": "admin@administrator.com",
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "created_at": "2026-01-20 10:30:00.123456+00:00"
}
```

**curl Example:**
```bash
curl -k -X POST https://localhost:5001/fruit_products/refresh-token \
  -H "Authorization: Bearer <token>"
```

---

## Private Endpoints (Admin Only)

### 3. Registration Management

#### GET All Registrations
**GET** `/fruit_products/register`

**Access:** Administrator only

**Success Response (200):**
```json
[
    {
        "registration_id": 1,
        "email": "admin@administrator.com",
        "created_at": "2026-01-20 10:30:00.123456+00:00",
        "updated_at": null,
        "user": {
            "id": 1,
            "user_name": "Admin User"
        }
    }
]
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/register \
  -H "Authorization: Bearer <admin_token>"
```

---

#### GET Registration by ID
**GET** `/fruit_products/register/<id>`

**Access:** Administrator only

**Success Response (200):**
```json
{
    "registration_id": 1,
    "email": "admin@administrator.com",
    "created_at": "2026-01-20 10:30:00.123456+00:00",
    "updated_at": null
}
```

**Error Response (404):**
```json
{
    "error": "Registration not found"
}
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/register/1 \
  -H "Authorization: Bearer <admin_token>"
```

---

#### POST Create Registration
**POST** `/fruit_products/register`

**Access:** Administrator only

**Request Body:**
```json
{
    "email": "newclient@example.com",
    "password": "SecurePassword123!",
    "role": "client"
}
```

**Success Response (201):**
```json
{
    "id": 2,
    "email": "newclient@example.com",
    "token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "created_at": "2026-01-20 10:30:00.123456+00:00"
}
```

**Error Response (409):**
```json
{
    "error": "User already exists or violates database constraints"
}
```

**curl Example:**
```bash
curl -k -X POST https://localhost:5001/fruit_products/register \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"email": "newclient@example.com", "password": "SecurePassword123!", "role": "client"}'
```

---

#### PUT Update Registration
**PUT** `/fruit_products/register/<id>`

**Access:** Administrator only

**Request Body:**
```json
{
    "email": "updated@example.com",
    "role": "administrator"
}
```

**Success Response (200):**
```json
{
    "message": "Registration with ID 2 has been UPDATED"
}
```

**curl Example:**
```bash
curl -k -X PUT https://localhost:5001/fruit_products/register/2 \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"email": "updated@example.com"}'
```

---

#### DELETE Registration
**DELETE** `/fruit_products/register/<id>`

**Access:** Administrator only

**Success Response (200):**
```json
{
    "message": "Registration with ID 2 has been DELETED"
}
```

**curl Example:**
```bash
curl -k -X DELETE https://localhost:5001/fruit_products/register/2 \
  -H "Authorization: Bearer <admin_token>"
```

---

### 4. Address Management

#### GET All Addresses
**GET** `/fruit_products/addresses`

**Access:** Administrator only

**Success Response (200):**
```json
[
    {
        "id": 1,
        "postal_code": "10001",
        "country": "USA",
        "state": "New York",
        "city": "New York City",
        "street": "123 Main Street",
        "created_at": "2026-01-20 10:30:00.123456+00:00",
        "updated_at": null,
        "users": [
            {
                "id": 1,
                "user_name": "John Doe"
            }
        ]
    }
]
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/addresses \
  -H "Authorization: Bearer <admin_token>"
```

---

#### GET Address by ID
**GET** `/fruit_products/addresses/<id>`

**Access:** Administrator only

**Success Response (200):**
```json
{
    "id": 1,
    "postal_code": "10001",
    "country": "USA",
    "state": "New York",
    "city": "New York City",
    "street": "123 Main Street",
    "created_at": "2026-01-20 10:30:00.123456+00:00",
    "updated_at": null
}
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/addresses/1 \
  -H "Authorization: Bearer <admin_token>"
```

---

#### POST Create Address
**POST** `/fruit_products/addresses`

**Access:** Administrator only

**Request Body:**
```json
{
    "street": "456 Oak Avenue",
    "city": "Los Angeles",
    "state": "California",
    "postal_code": "90001",
    "country": "USA"
}
```

**Success Response (200):**
```json
{
    "id": 2,
    "postal_code": "90001",
    "country": "USA",
    "state": "California",
    "created_at": "2026-01-20 10:30:00.123456+00:00"
}
```

**curl Example:**
```bash
curl -k -X POST https://localhost:5001/fruit_products/addresses \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"street": "456 Oak Avenue", "city": "Los Angeles", "state": "California", "postal_code": "90001", "country": "USA"}'
```

---

#### PUT Update Address
**PUT** `/fruit_products/addresses/<id>`

**Access:** Administrator only

**Request Body:**
```json
{
    "street": "789 Pine Street",
    "city": "San Francisco"
}
```

**Success Response (200):**
```json
{
    "message": "Address with ID 2 has been UPDATED"
}
```

**curl Example:**
```bash
curl -k -X PUT https://localhost:5001/fruit_products/addresses/2 \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"street": "789 Pine Street", "city": "San Francisco"}'
```

---

#### DELETE Address
**DELETE** `/fruit_products/addresses/<id>`

**Access:** Administrator only

**Success Response (200):**
```json
{
    "message": "Address with ID 2 has been DELETED"
}
```

**curl Example:**
```bash
curl -k -X DELETE https://localhost:5001/fruit_products/addresses/2 \
  -H "Authorization: Bearer <admin_token>"
```

---

### 5. User Management

#### GET All Users
**GET** `/fruit_products/users`

**Access:** Administrator only

**Success Response (200):**
```json
[
    {
        "id": 1,
        "registration_id": 2,
        "first_name": "John",
        "last_name": "Doe",
        "telephone": "12345678",
        "address_id": 1,
        "created_at": "2026-01-20 10:30:00.123456+00:00",
        "updated_at": null,
        "address": {
            "id": 1,
            "city": "New York City",
            "state": "New York"
        }
    }
]
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/users \
  -H "Authorization: Bearer <admin_token>"
```

---

#### GET User by ID
**GET** `/fruit_products/users/<id>`

**Access:** Administrator only

**Success Response (200):**
```json
{
    "id": 1,
    "registration_id": 2,
    "first_name": "John",
    "last_name": "Doe",
    "telephone": "12345678",
    "address_id": 1,
    "created_at": "2026-01-20 10:30:00.123456+00:00"
}
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/users/1 \
  -H "Authorization: Bearer <admin_token>"
```

---

#### POST Create User
**POST** `/fruit_products/users`

**Access:** Administrator only

**Request Body:**
```json
{
    "registration_id": 2,
    "first_name": "John",
    "last_name": "Doe",
    "telephone": "12345678",
    "address_id": 1
}
```

**Success Response (200):**
```json
{
    "id": 1,
    "registration_id": 2,
    "first_name": "John",
    "last_name": "Doe",
    "telephone": "12345678",
    "created_at": "2026-01-20 10:30:00.123456+00:00"
}
```

**curl Example:**
```bash
curl -k -X POST https://localhost:5001/fruit_products/users \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"registration_id": 2, "first_name": "John", "last_name": "Doe", "telephone": "12345678", "address_id": 1}'
```

---

#### PUT Update User
**PUT** `/fruit_products/users/<id>`

**Access:** Administrator only

**Request Body:**
```json
{
    "first_name": "Jane",
    "telephone": "87654321"
}
```

**Success Response (200):**
```json
{
    "message": "User with ID 1 has been UPDATED"
}
```

**curl Example:**
```bash
curl -k -X PUT https://localhost:5001/fruit_products/users/1 \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Jane", "telephone": "87654321"}'
```

---

#### DELETE User
**DELETE** `/fruit_products/users/<id>`

**Access:** Administrator only

**Success Response (200):**
```json
{
    "message": "User with ID 1 has been DELETED"
}
```

**curl Example:**
```bash
curl -k -X DELETE https://localhost:5001/fruit_products/users/1 \
  -H "Authorization: Bearer <admin_token>"
```

---

### 6. Product Management

#### GET All Products
**GET** `/fruit_products/products`

**Access:** Administrator only

**Success Response (200):**
```json
[
    {
        "id": 1,
        "name": "Apple",
        "description": "Fresh red apples",
        "price": 150,
        "size": "medium",
        "quantity": 100,
        "created_at": "2026-01-20 10:30:00.123456+00:00",
        "updated_at": null,
        "cart_products": []
    }
]
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/products \
  -H "Authorization: Bearer <admin_token>"
```

---

#### GET Product by ID
**GET** `/fruit_products/products/<id>`

**Access:** Administrator only

**Success Response (200):**
```json
{
    "id": 1,
    "name": "Apple",
    "description": "Fresh red apples",
    "price": 150,
    "size": "medium",
    "quantity": 100,
    "created_at": "2026-01-20 10:30:00.123456+00:00"
}
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/products/1 \
  -H "Authorization: Bearer <admin_token>"
```

---

#### POST Create Products
**POST** `/fruit_products/products`

**Access:** Administrator only

**Request Body (list of products):**
```json
[
    {
        "name": "Apple",
        "description": "Fresh red apples",
        "price": 150,
        "size": "medium",
        "quantity": 100
    },
    {
        "name": "Banana",
        "description": "Yellow bananas",
        "price": 100,
        "size": "large",
        "quantity": 200
    }
]
```

**Success Response (200):**
```json
[
    {
        "id": 1,
        "name": "Apple",
        "description": "Fresh red apples",
        "price": 150,
        "size": "medium",
        "quantity": 100,
        "created_at": "2026-01-20 10:30:00.123456+00:00",
        "updated_at": null
    },
    {
        "id": 2,
        "name": "Banana",
        "description": "Yellow bananas",
        "price": 100,
        "size": "large",
        "quantity": 200,
        "created_at": "2026-01-20 10:30:00.123456+00:00",
        "updated_at": null
    }
]
```

**curl Example:**
```bash
curl -k -X POST https://localhost:5001/fruit_products/products \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '[{"name": "Apple", "description": "Fresh red apples", "price": 150, "size": "medium", "quantity": 100}]'
```

---

#### PUT Update Product
**PUT** `/fruit_products/products/<id>`

**Access:** Administrator only

**Request Body:**
```json
{
    "price": 175,
    "quantity": 80
}
```

**Success Response (200):**
```json
{
    "id": 1,
    "name": "Apple",
    "price": 175,
    "quantity": 80,
    "size": "medium",
    "updated_at": "2026-01-20 11:00:00.123456+00:00"
}
```

**curl Example:**
```bash
curl -k -X PUT https://localhost:5001/fruit_products/products/1 \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"price": 175, "quantity": 80}'
```

---

#### DELETE Product
**DELETE** `/fruit_products/products/<id>`

**Access:** Administrator only

**Success Response (200):**
```json
{
    "message": "Product with ID 1 with name Apple has been DELETED"
}
```

**curl Example:**
```bash
curl -k -X DELETE https://localhost:5001/fruit_products/products/1 \
  -H "Authorization: Bearer <admin_token>"
```

---

### 7. Shopping Cart Management

#### GET All Shopping Carts
**GET** `/fruit_products/shopping_carts`

**Access:** Administrator or Client

**Success Response (200):**
```json
[
    {
        "id": 1,
        "user_id": 1,
        "status": "active",
        "purchase_date": "2026-01-20 10:30:00.123456+00:00",
        "created_at": "2026-01-20 10:30:00.123456+00:00",
        "updated_at": null,
        "receipt": {
            "receipt_id": 1,
            "payment_method": "cash",
            "total_amount": 450,
            "created_at": "2026-01-20 10:30:00.123456+00:00",
            "updated_at": null
        },
        "shopping_cart_products": [
            {
                "cart_id": 1,
                "product_id": 1,
                "quantity": 3,
                "created_at": "2026-01-20 10:30:00.123456+00:00",
                "updated_at": null
            }
        ]
    }
]
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/shopping_carts \
  -H "Authorization: Bearer <token>"
```

---

#### GET Shopping Cart by ID
**GET** `/fruit_products/shopping_carts/<id>`

**Access:** Administrator or Client

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/shopping_carts/1 \
  -H "Authorization: Bearer <token>"
```

---

#### PUT Update Shopping Cart
**PUT** `/fruit_products/shopping_carts/<id>`

**Access:** Administrator only

**Request Body:**
```json
{
    "status": "completed"
}
```

**curl Example:**
```bash
curl -k -X PUT https://localhost:5001/fruit_products/shopping_carts/1 \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"status": "completed"}'
```

---

#### DELETE Shopping Cart
**DELETE** `/fruit_products/shopping_carts/<id>`

**Access:** Administrator only

**curl Example:**
```bash
curl -k -X DELETE https://localhost:5001/fruit_products/shopping_carts/1 \
  -H "Authorization: Bearer <admin_token>"
```

---

### 8. Receipt Management

#### GET All Receipts
**GET** `/fruit_products/receipts`

**Access:** Administrator only

**Success Response (200):**
```json
[
    {
        "id": 1,
        "cart_id": 1,
        "payment_method": "cash",
        "total_amount": 450,
        "created_at": "2026-01-20 10:30:00.123456+00:00",
        "updated_at": null
    }
]
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/receipts \
  -H "Authorization: Bearer <admin_token>"
```

---

#### GET Receipt by ID
**GET** `/fruit_products/receipts/<id>`

**Access:** Administrator only

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/receipts/1 \
  -H "Authorization: Bearer <admin_token>"
```

---

#### POST Create Receipt
**POST** `/fruit_products/receipts`

**Access:** Administrator only

**Request Body:**
```json
{
    "cart_id": 1,
    "payment_method": "credit_card",
    "total_amount": 500
}
```

**curl Example:**
```bash
curl -k -X POST https://localhost:5001/fruit_products/receipts \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"cart_id": 1, "payment_method": "credit_card", "total_amount": 500}'
```

---

#### PUT Update Receipt
**PUT** `/fruit_products/receipts/<id>`

**Access:** Administrator only

**Request Body:**
```json
{
    "payment_method": "debit_card",
    "total_amount": 550
}
```

**curl Example:**
```bash
curl -k -X PUT https://localhost:5001/fruit_products/receipts/1 \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"payment_method": "debit_card", "total_amount": 550}'
```

---

#### DELETE Receipt
**DELETE** `/fruit_products/receipts/<id>`

**Access:** Administrator only

**curl Example:**
```bash
curl -k -X DELETE https://localhost:5001/fruit_products/receipts/1 \
  -H "Authorization: Bearer <admin_token>"
```

---

### 9. Shopping Cart Product Management

#### GET All Cart Products
**GET** `/fruit_products/shopping_cart_products`

**Access:** Administrator only

**Success Response (200):**
```json
[
    {
        "id": 1,
        "cart_id": 1,
        "product_id": 1,
        "checkout": false,
        "created_at": "2026-01-20 10:30:00.123456+00:00",
        "updated_at": null
    }
]
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/shopping_cart_products \
  -H "Authorization: Bearer <admin_token>"
```

---

#### POST Create Cart Product
**POST** `/fruit_products/shopping_cart_products`

**Access:** Administrator only

**Request Body:**
```json
{
    "cart_id": 1,
    "product_id": 2,
    "quantity": 5,
    "checkout": false
}
```

**curl Example:**
```bash
curl -k -X POST https://localhost:5001/fruit_products/shopping_cart_products \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"cart_id": 1, "product_id": 2, "quantity": 5, "checkout": false}'
```

---

#### PUT Update Cart Product
**PUT** `/fruit_products/shopping_cart_products/<id>`

**Access:** Administrator only

**Request Body:**
```json
{
    "quantity": 10,
    "checkout": true
}
```

**curl Example:**
```bash
curl -k -X PUT https://localhost:5001/fruit_products/shopping_cart_products/1 \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 10, "checkout": true}'
```

---

#### DELETE Cart Product
**DELETE** `/fruit_products/shopping_cart_products/<id>`

**Access:** Administrator only

**curl Example:**
```bash
curl -k -X DELETE https://localhost:5001/fruit_products/shopping_cart_products/1 \
  -H "Authorization: Bearer <admin_token>"
```

---

## Private Endpoints (Admin & Client)

### 10. Current User Info
**GET** `/fruit_products/me`

**Access:** Administrator or Client

**Success Response (200):**
```json
{
    "email": "client@example.com",
    "created_at": "2026-01-20 10:30:00.123456+00:00"
}
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/me \
  -H "Authorization: Bearer <token>"
```

---

### 11. Buy Fruits (Public Purchase API)

#### GET Purchase History
**GET** `/fruit_products/buy-fruits`

**Access:** Administrator or Client

Get all purchase receipts for the authenticated user.

**Success Response (200):**
```json
[
    {
        "id": 1,
        "cart_id": 1,
        "payment_method": "cash",
        "created_at": "2026-01-20 10:30:00.123456+00:00",
        "updated_at": null,
        "carts": [
            {
                "id": 1,
                "user_id": 1,
                "status": "active",
                "purchase_date": "2026-01-20 10:30:00.123456+00:00",
                "created_at": "2026-01-20 10:30:00.123456+00:00",
                "updated_at": null
            }
        ]
    }
]
```

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/buy-fruits \
  -H "Authorization: Bearer <token>"
```

---

#### GET Purchase by ID
**GET** `/fruit_products/buy-fruits/<id>`

**Access:** Administrator or Client

**curl Example:**
```bash
curl -k -X GET https://localhost:5001/fruit_products/buy-fruits/1 \
  -H "Authorization: Bearer <token>"
```

---

#### POST Purchase Fruits
**POST** `/fruit_products/buy-fruits`

**Access:** Administrator or Client

Purchase fruits. Creates shopping cart, cart products, and receipt.

**Request Body (list of items):**
```json
[
    {
        "name": "Apple",
        "size": "medium",
        "quantity": 3
    },
    {
        "name": "Banana",
        "size": "large",
        "quantity": 2
    }
]
```

**Success Response (201):**
```json
{
    "cart": {
        "id": 1,
        "user_id": 1,
        "status": "active",
        "purchase_date": "2026-01-20 10:30:00.123456+00:00",
        "created_at": "2026-01-20 10:30:00.123456+00:00"
    },
    "cart_products": [
        {
            "id": 1,
            "cart_id": 1,
            "product_id": 1,
            "quantity": 3,
            "checkout": false,
            "created_at": "2026-01-20 10:30:00.123456+00:00"
        },
        {
            "id": 2,
            "cart_id": 1,
            "product_id": 2,
            "quantity": 2,
            "checkout": false,
            "created_at": "2026-01-20 10:30:00.123456+00:00"
        }
    ],
    "receipt": {
        "id": 1,
        "cart_id": 1,
        "payment_method": "cash",
        "total_amount": 650,
        "created_at": "2026-01-20 10:30:00.123456+00:00"
    }
}
```

**Error Responses:**
- `400`: Invalid JSON format or validation error
- `404`: Product not found or user not found

**curl Example:**
```bash
curl -k -X POST https://localhost:5001/fruit_products/buy-fruits \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '[{"name": "Apple", "size": "medium", "quantity": 3}]'
```

---

#### DELETE Purchase
**DELETE** `/fruit_products/buy-fruits/<id>`

**Access:** Administrator only

**curl Example:**
```bash
curl -k -X DELETE https://localhost:5001/fruit_products/buy-fruits/1 \
  -H "Authorization: Bearer <admin_token>"
```

---

## Test Datasets

### Complete Test Dataset for Initial Setup

Execute these commands in order to set up a complete test environment:

#### Step 1: Login as Admin
```bash
# Get admin token
ADMIN_TOKEN=$(curl -sk -X POST https://localhost:5001/fruit_products/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@administrator.com", "password": "Just0n3Adm1inP455word"}' \
  | jq -r '.token')

echo "Admin Token: $ADMIN_TOKEN"
```

#### Step 2: Create Addresses
```bash
# Address 1 - New York
curl -k -X POST https://localhost:5001/fruit_products/addresses \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "street": "123 Main Street",
    "city": "New York City",
    "state": "New York",
    "postal_code": "10001",
    "country": "USA"
  }'

# Address 2 - Los Angeles
curl -k -X POST https://localhost:5001/fruit_products/addresses \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "street": "456 Hollywood Blvd",
    "city": "Los Angeles",
    "state": "California",
    "postal_code": "90028",
    "country": "USA"
  }'

# Address 3 - Chicago
curl -k -X POST https://localhost:5001/fruit_products/addresses \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "street": "789 Michigan Ave",
    "city": "Chicago",
    "state": "Illinois",
    "postal_code": "60611",
    "country": "USA"
  }'
```

#### Step 3: Create Client Registrations
```bash
# Client 1
curl -k -X POST https://localhost:5001/fruit_products/register \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john.doe@example.com",
    "password": "JohnSecure123!",
    "role": "client"
  }'

# Client 2
curl -k -X POST https://localhost:5001/fruit_products/register \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "jane.smith@example.com",
    "password": "JaneSecure456!",
    "role": "client"
  }'

# Client 3
curl -k -X POST https://localhost:5001/fruit_products/register \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "bob.wilson@example.com",
    "password": "BobSecure789!",
    "role": "client"
  }'
```

#### Step 4: Create User Profiles
```bash
# User 1 - John Doe
curl -k -X POST https://localhost:5001/fruit_products/users \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "registration_id": 2,
    "first_name": "John",
    "last_name": "Doe",
    "telephone": "55512345",
    "address_id": 1
  }'

# User 2 - Jane Smith
curl -k -X POST https://localhost:5001/fruit_products/users \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "registration_id": 3,
    "first_name": "Jane",
    "last_name": "Smith",
    "telephone": "55567890",
    "address_id": 2
  }'

# User 3 - Bob Wilson
curl -k -X POST https://localhost:5001/fruit_products/users \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "registration_id": 4,
    "first_name": "Bob",
    "last_name": "Wilson",
    "telephone": "55511223",
    "address_id": 3
  }'
```

#### Step 5: Create Products
```bash
curl -k -X POST https://localhost:5001/fruit_products/products \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {"name": "Apple", "description": "Fresh red apples from Washington", "price": 150, "size": "small", "quantity": 100},
    {"name": "Apple", "description": "Fresh red apples from Washington", "price": 250, "size": "medium", "quantity": 80},
    {"name": "Apple", "description": "Fresh red apples from Washington", "price": 350, "size": "large", "quantity": 50},
    {"name": "Banana", "description": "Organic yellow bananas", "price": 100, "size": "small", "quantity": 200},
    {"name": "Banana", "description": "Organic yellow bananas", "price": 150, "size": "medium", "quantity": 150},
    {"name": "Banana", "description": "Organic yellow bananas", "price": 200, "size": "large", "quantity": 100},
    {"name": "Orange", "description": "Fresh Florida oranges", "price": 175, "size": "small", "quantity": 120},
    {"name": "Orange", "description": "Fresh Florida oranges", "price": 275, "size": "medium", "quantity": 90},
    {"name": "Orange", "description": "Fresh Florida oranges", "price": 375, "size": "large", "quantity": 60},
    {"name": "Mango", "description": "Tropical mangoes from Mexico", "price": 300, "size": "small", "quantity": 75},
    {"name": "Mango", "description": "Tropical mangoes from Mexico", "price": 450, "size": "medium", "quantity": 50},
    {"name": "Mango", "description": "Tropical mangoes from Mexico", "price": 600, "size": "large", "quantity": 30},
    {"name": "Grape", "description": "California seedless grapes", "price": 200, "size": "small", "quantity": 80},
    {"name": "Grape", "description": "California seedless grapes", "price": 350, "size": "medium", "quantity": 60},
    {"name": "Grape", "description": "California seedless grapes", "price": 500, "size": "large", "quantity": 40}
  ]'
```

#### Step 6: Test Client Purchase
```bash
# Login as client
CLIENT_TOKEN=$(curl -sk -X POST https://localhost:5001/fruit_products/login \
  -H "Content-Type: application/json" \
  -d '{"email": "john.doe@example.com", "password": "JohnSecure123!"}' \
  | jq -r '.token')

echo "Client Token: $CLIENT_TOKEN"

# Make a purchase
curl -k -X POST https://localhost:5001/fruit_products/buy-fruits \
  -H "Authorization: Bearer $CLIENT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '[
    {"name": "Apple", "size": "medium", "quantity": 3},
    {"name": "Banana", "size": "large", "quantity": 2},
    {"name": "Orange", "size": "small", "quantity": 5}
  ]'
```

---

## Testing Plan

### Phase 1: Environment Setup

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 1.1 | Start PostgreSQL Docker container | Container running on port 5452 | ⬜ |
| 1.2 | Run `python main.py` | Server starts on https://localhost:5001 | ⬜ |
| 1.3 | Verify SSL certificate | Browser/curl shows certificate warning | ⬜ |

### Phase 2: Authentication Testing

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 2.1 | POST /login with valid admin credentials | Returns 200 with JWT token | ⬜ |
| 2.2 | POST /login with invalid email | Returns 404 User not found | ⬜ |
| 2.3 | POST /login with invalid password | Returns 403 Invalid password | ⬜ |
| 2.4 | GET /me with valid token | Returns 200 with user info | ⬜ |
| 2.5 | GET /me without token | Returns 401 Unauthorized | ⬜ |
| 2.6 | POST /refresh-token with valid token | Returns new tokens | ⬜ |

### Phase 3: Address CRUD Testing (Admin Only)

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 3.1 | POST /addresses (create) | Returns 200 with new address | ⬜ |
| 3.2 | POST /addresses (duplicate) | Returns 409 constraint error | ⬜ |
| 3.3 | GET /addresses | Returns list of addresses | ⬜ |
| 3.4 | GET /addresses/1 | Returns single address | ⬜ |
| 3.5 | GET /addresses/999 | Returns 404 not found | ⬜ |
| 3.6 | PUT /addresses/1 | Returns 200 updated message | ⬜ |
| 3.7 | DELETE /addresses/1 | Returns 200 deleted message | ⬜ |
| 3.8 | Access with client token | Returns 403 Forbidden | ⬜ |

### Phase 4: Registration CRUD Testing (Admin Only)

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 4.1 | POST /register (create client) | Returns 201 with token | ⬜ |
| 4.2 | POST /register (create admin) | Returns 201 with token | ⬜ |
| 4.3 | POST /register (duplicate email) | Returns 409 constraint error | ⬜ |
| 4.4 | GET /register | Returns list of registrations | ⬜ |
| 4.5 | GET /register/2 | Returns single registration | ⬜ |
| 4.6 | PUT /register/2 | Returns 200 updated message | ⬜ |
| 4.7 | DELETE /register/2 | Returns 200 deleted message | ⬜ |

### Phase 5: User CRUD Testing (Admin Only)

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 5.1 | POST /users (create) | Returns 200 with new user | ⬜ |
| 5.2 | POST /users (invalid registration_id) | Returns error | ⬜ |
| 5.3 | GET /users | Returns list of users | ⬜ |
| 5.4 | GET /users/1 | Returns single user | ⬜ |
| 5.5 | PUT /users/1 | Returns 200 updated message | ⬜ |
| 5.6 | DELETE /users/1 | Returns 200 deleted message | ⬜ |

### Phase 6: Product CRUD Testing (Admin Only)

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 6.1 | POST /products (create list) | Returns 200 with products | ⬜ |
| 6.2 | POST /products (single item) | Returns 400 requires list | ⬜ |
| 6.3 | GET /products | Returns list of products | ⬜ |
| 6.4 | GET /products/1 | Returns single product | ⬜ |
| 6.5 | PUT /products/1 (update price) | Returns 200 with updated data | ⬜ |
| 6.6 | PUT /products/1 (update quantity) | Returns 200 with updated data | ⬜ |
| 6.7 | DELETE /products/1 | Returns 200 deleted message | ⬜ |

### Phase 7: Shopping Cart Testing (Admin & Client)

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 7.1 | GET /shopping_carts | Returns list of carts | ⬜ |
| 7.2 | GET /shopping_carts/1 | Returns single cart with details | ⬜ |
| 7.3 | PUT /shopping_carts/1 (admin) | Returns 200 updated | ⬜ |
| 7.4 | DELETE /shopping_carts/1 (admin) | Returns 200 deleted | ⬜ |

### Phase 8: Receipt Testing (Admin Only)

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 8.1 | GET /receipts | Returns list of receipts | ⬜ |
| 8.2 | GET /receipts/1 | Returns single receipt | ⬜ |
| 8.3 | POST /receipts | Returns 200 with new receipt | ⬜ |
| 8.4 | PUT /receipts/1 | Returns 200 updated | ⬜ |
| 8.5 | DELETE /receipts/1 | Returns 200 deleted | ⬜ |

### Phase 9: Cart Products Testing (Admin Only)

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 9.1 | GET /shopping_cart_products | Returns list | ⬜ |
| 9.2 | GET /shopping_cart_products/1 | Returns single item | ⬜ |
| 9.3 | POST /shopping_cart_products | Returns 200 with new item | ⬜ |
| 9.4 | PUT /shopping_cart_products/1 | Returns 200 updated | ⬜ |
| 9.5 | DELETE /shopping_cart_products/1 | Returns 200 deleted | ⬜ |

### Phase 10: Buy Fruits Integration Testing (Admin & Client)

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 10.1 | POST /buy-fruits (valid order) | Returns 201 with cart, products, receipt | ⬜ |
| 10.2 | POST /buy-fruits (invalid product) | Returns 404 product not found | ⬜ |
| 10.3 | POST /buy-fruits (invalid size) | Returns 400 validation error | ⬜ |
| 10.4 | POST /buy-fruits (invalid quantity) | Returns 400 validation error | ⬜ |
| 10.5 | POST /buy-fruits (single item) | Returns 400 requires list | ⬜ |
| 10.6 | GET /buy-fruits | Returns purchase history | ⬜ |
| 10.7 | GET /buy-fruits/1 | Returns single purchase | ⬜ |
| 10.8 | DELETE /buy-fruits/1 (admin) | Returns 200 deleted | ⬜ |

### Phase 11: Authorization Testing

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 11.1 | Client access to admin-only endpoint | Returns 403 Forbidden | ⬜ |
| 11.2 | No token access to protected endpoint | Returns 401 Unauthorized | ⬜ |
| 11.3 | Expired token access | Returns 401 Unauthorized | ⬜ |
| 11.4 | Invalid token access | Returns 401 Unauthorized | ⬜ |

### Phase 12: Edge Cases & Error Handling

| Step | Action | Expected Result | Status |
|------|--------|-----------------|--------|
| 12.1 | POST with invalid JSON | Returns 400 Bad Request | ⬜ |
| 12.2 | PUT non-existent resource | Returns 404 Not Found | ⬜ |
| 12.3 | DELETE non-existent resource | Returns 404 Not Found | ⬜ |
| 12.4 | GET with invalid ID format | Returns 404 or 400 | ⬜ |
| 12.5 | POST with missing required fields | Returns 400 Bad Request | ⬜ |
| 12.6 | POST with invalid field types | Returns 400 Bad Request | ⬜ |

---

## Quick Reference - All Endpoints Summary

| Endpoint | Method | Access | Description |
|----------|--------|--------|-------------|
| `/login` | POST | Public | Authenticate user |
| `/refresh-token` | POST | Auth | Refresh JWT tokens |
| `/me` | GET | Auth | Get current user info |
| `/register` | GET | Admin | List all registrations |
| `/register` | POST | Admin | Create registration |
| `/register/<id>` | GET | Admin | Get registration by ID |
| `/register/<id>` | PUT | Admin | Update registration |
| `/register/<id>` | DELETE | Admin | Delete registration |
| `/addresses` | GET | Admin | List all addresses |
| `/addresses` | POST | Admin | Create address |
| `/addresses/<id>` | GET | Admin | Get address by ID |
| `/addresses/<id>` | PUT | Admin | Update address |
| `/addresses/<id>` | DELETE | Admin | Delete address |
| `/users` | GET | Admin | List all users |
| `/users` | POST | Admin | Create user |
| `/users/<id>` | GET | Admin | Get user by ID |
| `/users/<id>` | PUT | Admin | Update user |
| `/users/<id>` | DELETE | Admin | Delete user |
| `/products` | GET | Admin | List all products |
| `/products` | POST | Admin | Create products (list) |
| `/products/<id>` | GET | Admin | Get product by ID |
| `/products/<id>` | PUT | Admin | Update product |
| `/products/<id>` | DELETE | Admin | Delete product |
| `/shopping_carts` | GET | Auth | List shopping carts |
| `/shopping_carts` | POST | Auth | Create shopping cart |
| `/shopping_carts/<id>` | GET | Auth | Get cart by ID |
| `/shopping_carts/<id>` | PUT | Admin | Update cart |
| `/shopping_carts/<id>` | DELETE | Admin | Delete cart |
| `/receipts` | GET | Admin | List all receipts |
| `/receipts` | POST | Admin | Create receipt |
| `/receipts/<id>` | GET | Admin | Get receipt by ID |
| `/receipts/<id>` | PUT | Admin | Update receipt |
| `/receipts/<id>` | DELETE | Admin | Delete receipt |
| `/shopping_cart_products` | GET | Admin | List cart products |
| `/shopping_cart_products` | POST | Admin | Create cart product |
| `/shopping_cart_products/<id>` | GET | Admin | Get cart product by ID |
| `/shopping_cart_products/<id>` | PUT | Admin | Update cart product |
| `/shopping_cart_products/<id>` | DELETE | Admin | Delete cart product |
| `/buy-fruits` | GET | Auth | Get purchase history |
| `/buy-fruits` | POST | Auth | Make a purchase |
| `/buy-fruits/<id>` | GET | Auth | Get purchase by ID |
| `/buy-fruits/<id>` | PUT | Auth | Update purchase |
| `/buy-fruits/<id>` | DELETE | Admin | Delete purchase |

---

## Default Admin Credentials

| Field | Value |
|-------|-------|
| Email | `admin@administrator.com` |
| Password | `Just0n3Adm1inP455word` |
| Role | `administrator` |

> **Note:** These credentials are created automatically when the application starts.

---

## Valid Product Sizes

The following sizes are accepted for buy-fruits endpoint:
- `small`
- `medium`
- `large`

---

## Cart Status Values

| Status | Description |
|--------|-------------|
| `active` | Cart is active (default) |
| `pending` | Pending checkout |
| `completed` | Purchase completed |
| `cancelled` | Cart cancelled |
