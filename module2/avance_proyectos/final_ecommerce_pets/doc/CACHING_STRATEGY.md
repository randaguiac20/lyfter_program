# Caching Strategy - E-Commerce Pets API

## Overview

This API uses **Redis** as a caching layer to reduce database load on read-heavy endpoints. The `CacheManager` class (`modules/cache_manager.py`) wraps all Redis operations with error handling and graceful fallback to the database when Redis is unavailable.

**Pattern used:** Cache-Aside (Lazy Loading) — data is loaded from cache on read; on cache miss, data is fetched from DB and written to cache. Write operations invalidate relevant cache keys.

---

## Cached Endpoints

### 1. Products — `GET /e_commerce_pets/products` and `GET /e_commerce_pets/products/<id>`

| Property | Value |
|---|---|
| **Cache keys** | `products:{id}`, `products:all` |
| **TTL** | 300 seconds (5 minutes) |
| **Repository** | `repositories/product_repository.py` |

**Why cached:** The product catalog is the most read-heavy resource in the API. Every client browsing the store queries products. Product data changes infrequently — only administrators can create, update, or delete products. A 5-minute TTL provides a strong performance benefit while keeping data reasonably fresh.

**Invalidation conditions:**
| Operation | Keys invalidated |
|---|---|
| `POST /products` (create) | `products:*` (all product keys) |
| `PUT /products/<id>` (update) | `products:*` (all product keys) |
| `DELETE /products/<id>` (delete) | `products:*` (all product keys) |

**Why invalidate all keys on any write:** A single-product update affects both the individual cache (`products:{id}`) and the list cache (`products:all`) which contains that product's data. Invalidating all keys with a pattern ensures consistency.

---

### 2. Receipts — `GET /e_commerce_pets/receipts` and `GET /e_commerce_pets/receipts/<id>`

| Property | Value |
|---|---|
| **Cache keys** | `receipts:{id}`, `receipts:all` |
| **TTL** | 150 seconds (2.5 minutes) |
| **Repository** | `repositories/receipt_repository.py` |

**Why cached:** Receipts are financial records that are essentially immutable once created. They are queried for order history and reporting. The read-to-write ratio is high. A shorter TTL than products accounts for the fact that new receipts are created with each purchase.

**Invalidation conditions:**
| Operation | Keys invalidated |
|---|---|
| `POST /receipts` (create) | `receipts:*` (all receipt keys) |
| `PUT /receipts/<id>` (update) | `receipts:*` (all receipt keys) |
| `DELETE /receipts/<id>` (delete) | `receipts:*` (all receipt keys) |

---

### 3. Users — `GET /e_commerce_pets/users` and `GET /e_commerce_pets/users/<id>`

| Property | Value |
|---|---|
| **Cache keys** | `users:{id}`, `users:all` |
| **TTL** | 180 seconds (3 minutes) |
| **Repository** | `repositories/user_repository.py` |

**Why cached:** User profiles are queried by administrators for management operations. Profile data (name, telephone, address) changes occasionally but not frequently. The response includes embedded address and cart data via relationships. A 3-minute TTL balances freshness with reduced database load.

**Invalidation conditions:**
| Operation | Keys invalidated |
|---|---|
| `POST /users` (create) | `users:*` |
| `PUT /users/<id>` (update) | `users:*` |
| `DELETE /users/<id>` (delete) | `users:*` |
| Any address write (cross-invalidation) | `users:*` |

**Why cross-invalidation from addresses:** The user GET response embeds the full address object inline. If an address is updated but the user cache is not invalidated, clients will see stale address data in user responses until TTL expires.

---

### 4. Addresses — `GET /e_commerce_pets/addresses` and `GET /e_commerce_pets/addresses/<id>`

| Property | Value |
|---|---|
| **Cache keys** | `addresses:{id}`, `addresses:all` |
| **TTL** | 600 seconds (10 minutes) |
| **Repository** | `repositories/address_repository.py` |

**Why cached:** Addresses are reference data — street, city, state, and postal code rarely change once created. This is the most stable entity in the system, justifying the longest TTL. The 10-minute window provides significant reduction in database queries for what is essentially static data.

**Invalidation conditions:**
| Operation | Keys invalidated |
|---|---|
| `POST /addresses` (create) | `addresses:*` + `users:*` (cross-invalidation) |
| `PUT /addresses/<id>` (update) | `addresses:*` + `users:*` (cross-invalidation) |
| `DELETE /addresses/<id>` (delete) | `addresses:*` + `users:*` (cross-invalidation) |

---

## Non-Cached Endpoints

### 5. Registration — `GET/POST/PUT/DELETE /e_commerce_pets/register`

**Why NOT cached:** Registration handles authentication credentials (email, hashed password, role). Caching this data introduces security risks:
- A role change (e.g., revoking admin access) must take effect immediately
- Stale cached credentials could allow unauthorized access
- Registration is an admin-only, low-frequency operation — caching provides negligible performance benefit

### 6. Login — `POST /e_commerce_pets/login` and `GET /e_commerce_pets/me`

**Why NOT cached:**
- `POST /login`: Authentication **must always validate against the database**. Caching login responses could allow access with revoked or changed credentials. This is a critical security requirement.
- `GET /me`: Returns current user info from the JWT token. Each request is user-specific and infrequent. The overhead of cache key management per-user outweighs the minimal performance gain.

### 7. Refresh Token — `POST /e_commerce_pets/refresh-token`

**Why NOT cached:** Token generation must produce unique tokens per request for security. Caching token responses would reissue the same token to multiple requests, defeating the purpose of token refresh and creating a security vulnerability.

### 8. Shopping Carts — `GET/POST/PUT/DELETE /e_commerce_pets/shopping_carts`

**Why NOT cached:** Shopping carts are highly transactional entities with frequent state transitions (active -> pending -> completed -> cancelled). During an active shopping session:
- Items are added and removed constantly
- Cart status changes during checkout flow
- Cache would be invalidated on nearly every request, negating any benefit
- Stale cart data during checkout could cause incorrect order processing

The cost of cache invalidation complexity exceeds the performance benefit.

### 9. Shopping Cart Products — `GET/POST/PUT/DELETE /e_commerce_pets/shopping_cart_products`

**Why NOT cached:** This is a junction table that changes with every add/remove operation during shopping. Additionally, each change would require cross-invalidation of:
- `products:*` (product responses embed cart_products)
- `shopping_carts:*` (if cached, cart responses embed cart_products)

The cascading invalidation makes caching counterproductive.

---

## Cross-Invalidation Rules

| When this changes... | Also invalidate... | Reason |
|---|---|---|
| Address (POST/PUT/DELETE) | `users:*` | User GET responses embed full address objects |

---

## Error Handling

All cache operations are wrapped in `try/except redis.RedisError` blocks. On Redis failure:
1. **Cache reads:** Fall back to direct database query (application continues working)
2. **Cache writes/invalidation:** Log the error, continue without caching (data correctness preserved)

This ensures Redis outages do not cause application downtime.

---

## Key Naming Convention

| Pattern | Example | Usage |
|---|---|---|
| `{entity}:{id}` | `products:42` | Single record by ID |
| `{entity}:all` | `products:all` | Full list of records |
| `{entity}:*` | `products:*` | Wildcard for pattern-based invalidation |

---

## TTL Summary

| Entity | TTL | Justification |
|---|---|---|
| Products | 300s (5 min) | Read-heavy catalog, admin-only writes |
| Receipts | 150s (2.5 min) | Immutable records, new ones created on purchases |
| Users | 180s (3 min) | Moderate change frequency, includes embedded relations |
| Addresses | 600s (10 min) | Reference data, rarely changes |
