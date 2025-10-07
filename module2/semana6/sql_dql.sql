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
*/
DROP TABLE customers;
DROP TABLE products;
DROP TABLE inventory;
DROP TABLE orders;
DROP TABLE shipping;

SELECT * FROM customers;
SELECT * FROM products;
SELECT * FROM inventory;
SELECT * FROM orders;
SELECT * FROM shipping;
