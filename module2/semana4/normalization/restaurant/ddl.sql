DROP TABLE orders;
DROP TABLE customer_addresses;
DROP TABLE customers;
DROP TABLE products;
DROP TABLE order_products;

CREATE TABLE customers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL,
	phone_number VARCHAR(50) NOT NULL
);

CREATE TABLE customer_addresses (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INT NOT NULL,
	address VARCHAR(128) NOT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);

CREATE TABLE products (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL,
	price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE orders (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	customer_id INT NOT NULL,
	customer_address_id INT NOT NULL,
    special_request VARCHAR(50) DEFAULT NULL,
    delivery_time TEXT DEFAULT NULL,
    FOREIGN KEY(customer_id) REFERENCES customers(id),
	FOREIGN KEY(customer_address_id) REFERENCES customer_addresses(id)
);

CREATE TABLE order_products (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INT NOT NULL,
	product_id INT NOT NULL,
	quantity INT NOT NULL,
	FOREIGN KEY(order_id) REFERENCES orders(id),
	FOREIGN KEY(product_id) REFERENCES products(id)
);