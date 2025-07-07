-- SQLite
/*

Examples

SELECT name, last_name, history_score
	FROM students;

SELECT *
  FROM books
  GROUP BY author_id
  ORDER BY title DESC;

SELECT *
	FROM books
	WHERE author_id = 1;

SELECT title
	FROM authors
	ORDER BY title ASC;


SELECT
    receipts.id AS receipt_id,
    receipts.receipt_number,
    product_receipts.product_id as product_id_from_product_receipts,
    products.id AS product_id_from_products,
    receipts.total_amount
FROM receipts
INNER JOIN carts ON receipts.cart_id = carts.id
INNER JOIN product_receipts ON product_receipts.cart_id = carts.id
INNER JOIN products ON products.id = product_receipts.product_id
ORDER BY products.id;


>>>> DQL = Data Query Language

*/

/* 1. Obtenga todos los libros y sus autores*/
SELECT b.name AS book_name,
    a.name AS author_name
    FROM books b
LEFT JOIN authors a ON a.id = b.author_id;
/* 2. Obtenga todos los libros que no tienen autor*/
SELECT * FROM books
    WHERE author_id IS NULL;
/* 3. Obtenga todos los autores que no tienen libros*/
SELECT a.*
FROM authors a
LEFT JOIN books b ON a.id = b.author_id
WHERE b.author_id IS NULL;
/* 4. Obtenga todos los libros que han sido rentados en algún momento*/
SELECT b.name AS book_name
    FROM rents r
LEFT JOIN books b ON r.book_id = b.id
GROUP BY book_name;
/* 5. Obtenga todos los libros que nunca han sido rentados*/
SELECT b.id AS book_id,
    b.name AS book_name
    FROM books b
LEFT JOIN rents r ON b.id = r.book_id
WHERE r.book_id IS NULL
GROUP BY book_name;
/* 6. Obtenga todos los clientes que nunca han rentado un libro*/
SELECT c.id AS customer_id,
       c.name AS customer_name
    FROM customers c
LEFT JOIN rents r ON c.id = r.customer_id
WHERE r.customer_id IS NULL
GROUP BY customer_name;
/* 7. Obtenga todos los libros que han sido rentados y están en estado “Overdue”*/
SELECT r.id AS rent_id,
    b.name AS book_name,
    r.state
    FROM rents r
LEFT JOIN books b ON b.id = r.book_id
WHERE state = 'Overdue';