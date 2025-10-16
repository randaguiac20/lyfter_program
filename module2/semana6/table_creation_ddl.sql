/*
Examples:

# CREATE
CREATE TABLE users (
	id INT PRIMARY KEY,
	email VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE documents(
	id INT PRIMARY KEY,
	title VARCHAR(25) NOT NULL
);

CREATE TABLE user_documents(
	id INT PRIMARY KEY,
	user_id INT REFERENCES users (id),
	document_id INT REFERENCES documents(id)
);

ALTER TABLE product_receipts
	ADD cart_id;

DROP TABLE users;
DROP TABLE employees;
DROP TABLE products;
DROP TABLE carts;
DROP TABLE product_receipts;
DROP TABLE receipts;
*/
-- SQLite

CREATE TABLE customers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id VARCHAR(25) NOT NULL,
	name VARCHAR(25) NOT NULL,
	last_name VARCHAR(25) NOT NULL,
	address VARCHAR(255) UNIQUE NOT NULL,
	last_purchase TEXT DEFAULT (datetime('now')),
    last_modified TEXT DEFAULT (datetime('now'))
);

CREATE TABLE products (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	product_id CHAR(50) UNIQUE NOT NULL,
	name VARCHAR(25) UNIQUE NOT NULL,
    brand VARCHAR(25) NOT NULL,
    last_modified TEXT DEFAULT (datetime('now'))
);

CREATE TABLE inventory (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	product_id CHAR(50) UNIQUE NOT NULL,
	quantity SMALLINT(25) DEFAULT 0,
	ingress_date TEXT DEFAULT (datetime('now')),
    last_modified TEXT DEFAULT (datetime('now'))
);

CREATE TABLE orders (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	order_id VARCHAR(10) NOT NULL,
	customer_id INT NOT NULL,
    total BIGINT(25) DEFAULT 0,
    status VARCHAR(10) DEFAULT 'in_progress',
    FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE shipping (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	order_id VARCHAR(10) NOT NULL,
    address VARCHAR(255) UNIQUE NOT NULL,
	status VARCHAR(10) DEFAULT 'in_progress',
	last_modified TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(order_id) REFERENCES orders(order_id)
);
