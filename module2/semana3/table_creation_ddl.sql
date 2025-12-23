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


CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(25) NOT NULL,
	last_name VARCHAR(25) NOT NULL,
	phone_number VARCHAR(25) DEFAULT 'unknown',
	email VARCHAR(25) UNIQUE NOT NULL,
    last_modified TEXT DEFAULT (datetime('now'))
);

CREATE TABLE employees (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(10) DEFAULT 'unknown',
    role VARCHAR(25) DEFAULT 'unknown',
	name VARCHAR(25) NOT NULL,
	last_name VARCHAR(25) NOT NULL,
	phone_number VARCHAR(25) DEFAULT 'unknown',
	email VARCHAR(25) UNIQUE NOT NULL,
    last_modified TEXT DEFAULT (datetime('now'))
);

CREATE TABLE products (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	code CHAR(50) UNIQUE NOT NULL,
	name VARCHAR(25) UNIQUE NOT NULL,
    price SMALLINT(25) DEFAULT 0,
    brand VARCHAR(25) NOT NULL,
	ingress_date TEXT DEFAULT (datetime('now')),
    last_modified TEXT DEFAULT (datetime('now'))
);

CREATE TABLE carts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INT NOT NULL,
    product_receipt_code VARCHAR(25) DEFAULT 'null',
    last_modified TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(product_receipt_code) REFERENCES product_receipts(product_receipt_code)
);

CREATE TABLE product_receipts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	receipt_code VARCHAR(10) DEFAULT 'null',
    quantity INT DEFAULT 0,
	amount INT DEFAULT 0,
    taxes INT DEFAULT 0,
    client_phone_number VARCHAR(25) DEFAULT 'unknown',
    employeed_code VARCHAR(10) DEFAULT 'unknown',
    user_id INT NOT NULL,
	product_id INT NOT NULL,
	cart_id INT NOT NULL,
	status VARCHAR(10) DEFAULT 'in_progress',
	last_modified TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(client_phone_number) REFERENCES users(phone_number),
    FOREIGN KEY(employeed_code) REFERENCES employees(code),
    FOREIGN KEY(product_id) REFERENCES products(id),
	FOREIGN KEY(cart_id) REFERENCES carts(id)
);

CREATE TABLE receipts (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	receipt_number SMALLINT UNIQUE DEFAULT 0,
	purchase_data TEXT DEFAULT (datetime('now')),
    total_amount INT DEFAULT 0,
	cart_id INT NOT NULL,
	status VARCHAR(10) DEFAULT 'in_progress',
	last_modified TEXT DEFAULT (datetime('now')),
    FOREIGN KEY(cart_id) REFERENCES carts(id)
);