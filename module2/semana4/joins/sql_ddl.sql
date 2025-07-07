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

DROP TABLE books;
DROP TABLE authors;
DROP TABLE customers;
DROP TABLE rents;

>>>> DQL = Data Definition Language

*/

-- SQLite

CREATE TABLE books (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL,
	author_id INT DEFAULT NULL,
	FOREIGN KEY(author_id) REFERENCES authors(id)
);

CREATE TABLE authors (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50)
);

CREATE TABLE customers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(25) NOT NULL,
    email VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE rents (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	book_id INT NOT NULL,
	customer_id INT NOT NULL,
    state VARCHAR(25),
    FOREIGN KEY(book_id) REFERENCES books(id),
	FOREIGN KEY(customer_id) REFERENCES customers(id)
);
