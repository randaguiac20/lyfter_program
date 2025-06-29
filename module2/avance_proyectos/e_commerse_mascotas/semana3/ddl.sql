/*
Examples:
# CREATE
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email VARCHAR(25) UNIQUE NOT NULL
);
CREATE TABLE documents(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title VARCHAR(25) NOT NULL
);
CREATE TABLE user_documents(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INT REFERENCES users (id),
	document_id INT REFERENCES documents(id)
);
ALTER TABLE product_receipts
	ADD cart_id;

DROP TABLE breeds;
DROP TABLE users;
DROP TABLE roles;
DROP TABLE products;
DROP TABLE receipts;
DROP TABLE shooping_carts;
DROP TABLE shoopping_cart_products;
*/
-- SQLite


CREATE TABLE breeds (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(65) NOT NULL,
    size VARCHAR(25) NOT NULL,
    description CHAR(65) NOT NULL,
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE roles (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(65) NOT NULL,
    description CHAR(65) NOT NULL,
    updated_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email VARCHAR(25) UNIQUE NOT NULL,
    name CHAR(65) NOT NULL,
    lastname CHAR(65) NOT NULL,
    description CHAR(65) NOT NULL,
    role_id INT NOT NULL,
    status VARCHAR(25) NOT NULL,
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(role_id) REFERENCES roles(id)
);

CREATE TABLE products (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	sku VARCHAR(25) UNIQUE NOT NULL,
    name CHAR(65) NOT NULL,
    size VARCHAR(25) NOT NULL,
    description CHAR(65) NOT NULL,
    price FLOAT NOT NULL,
    brand CHAR(65) NOT NULL,
    breed_size_id INT NOT NULL,
    quantity INT DEFAULT 0,
    ingress_date TEXT DEFAULT (date('now')),
    expiration_date TEXT DEFAULT (date('now')),
    status VARCHAR(25) NOT NULL,
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(breed_size_id) REFERENCES breeds(id)
);

CREATE TABLE receipts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    cart_id INT NOT NULL,
    description CHAR(65) NOT NULL,
    payment_method VARCHAR(65) NOT NULL,
    total_amount FLOAT DEFAULT 0,
    purchase_date TEXT DEFAULT (date('now')),
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(cart_id) REFERENCES shooping_carts(id)
);

CREATE TABLE shoopping_cart_products (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INT NOT NULL,
    cart_id INT NOT NULL,
    quantity INT DEFAULT 0,
    checkout INT DEFAULT 0,
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(cart_id) REFERENCES shooping_carts(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE TABLE shooping_carts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INT NOT NULL,
    purchase_date TEXT DEFAULT (date('now')),
    status VARCHAR(25) NOT NULL,
    updated_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(user_id) REFERENCES users(id)
);