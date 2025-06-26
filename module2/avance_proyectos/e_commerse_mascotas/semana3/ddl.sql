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

DROP TABLE sizes;
DROP TABLE breeds;
DROP TABLE stores;
DROP TABLE users;
DROP TABLE roles;
DROP TABLE user_registrations;
DROP TABLE products;
DROP TABLE inventory;
DROP TABLE product_registrations;
DROP TABLE receipts;
DROP TABLE sales;
DROP TABLE carts;
*/
-- SQLite


CREATE TABLE sizes (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    size CHAR(65) NOT NULL,
    description CHAR(65) NOT NULL,
    lasttime_modified TEXT DEFAULT (datetime('now'))
);

CREATE TABLE breeds (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(65) NOT NULL,
    size_id INT NOT NULL,
    description CHAR(65) NOT NULL,
    lasttime_modified TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(size_id) REFERENCES sizes(id)
);

CREATE TABLE stores (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(65) NOT NULL,
    email CHAR(65) UNIQUE NOT NULL,
    description CHAR(65) NOT NULL,
    lasttime_modified TEXT DEFAULT (datetime('now'))
);

CREATE TABLE roles (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(65) NOT NULL,
    description CHAR(65) NOT NULL,
    lasttime_modified TEXT DEFAULT (datetime('now'))
);

CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	email VARCHAR(25) UNIQUE NOT NULL,
    name CHAR(65) NOT NULL,
    lastname CHAR(65) NOT NULL,
    description CHAR(65) NOT NULL,
    lasttime_modified TEXT DEFAULT (datetime('now'))
);

CREATE TABLE user_registrations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INT UNIQUE NOT NULL,
    role_id CHAR(65) NOT NULL,
    status VARCHAR(65) NOT NULL,
    lasttime_modified TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(role_id) REFERENCES roles(id)
);

CREATE TABLE products (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	sku VARCHAR(25) UNIQUE NOT NULL,
    name CHAR(65) NOT NULL,
    description CHAR(65) NOT NULL,
    brand CHAR(65) NOT NULL,
    price FLOAT NOT NULL,
    expiration_date TEXT DEFAULT (date('now')),
    size_id INT NOT NULL,
    breed_size_id INT NOT NULL,
    lasttime_modified TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(size_id) REFERENCES sizes(id),
    FOREIGN KEY(breed_size_id) REFERENCES breeds(id)
);

CREATE TABLE inventory (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INT NOT NULL,
    status VARCHAR(65) NOT NULL,
    description CHAR(65) NOT NULL,
    quantity INT DEFAULT 0,
    lasttime_modified TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(product_id) REFERENCES products(id)
);

CREATE TABLE product_registrations (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INT NOT NULL,
    inventory_id INT NOT NULL,
    description CHAR(65) NOT NULL,
    ingress_date TEXT DEFAULT (date('now')),
    lasttime_modified TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(product_id) REFERENCES products(id),
    FOREIGN KEY(inventory_id) REFERENCES inventory(id)
);

CREATE TABLE receipts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_number VARCHAR(25) UNIQUE NOT NULL,
    description CHAR(65) NOT NULL,
    total_amount FLOAT DEFAULT 0,
    lasttime_modified TEXT DEFAULT (datetime('now'))
);

CREATE TABLE sales (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INT NOT NULL,
    cart_reference_number VARCHAR(25) UNIQUE NOT NULL,
    lasttime_modified TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(receipt_id) REFERENCES receipts(id)
);

CREATE TABLE carts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference_number VARCHAR(50) NOT NULL,
    quantity INT DEFAULT 0,
    checkout INT DEFAULT 0,
    purchase_date TEXT DEFAULT (datetime('now')),
    receipt_id INT,
    sale_id INT,
    store_id INT NOT NULL,
    user_id INT NOT NULL,
    product_id INT NOT NULL,
    status VARCHAR(65) NOT NULL,
    lasttime_modified TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(receipt_id) REFERENCES receipts(id),
    FOREIGN KEY(sale_id) REFERENCES sales(id),
    FOREIGN KEY(store_id) REFERENCES stores(id),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
);