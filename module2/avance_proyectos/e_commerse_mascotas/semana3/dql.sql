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

SELECT * FROM breeds;
SELECT * FROM users;
SELECT * FROM roles;
SELECT * FROM products;
SELECT * FROM receipts;
SELECT * FROM shooping_carts;
SELECT * FROM shoopping_cart_products;

/*
THIS QUERY WILL GIVE YOU INFORMATION FOR THE FOLLOWING TABLES
  shooping_carts
  stores
*/

SELECT
    shooping_carts.user_id AS user_id,
    users.email AS user_email,
    shooping_carts.status AS status,
    receipts.total_amount
FROM receipts
INNER JOIN shooping_carts ON receipts.cart_id = shooping_carts.id
INNER JOIN users ON users.id = shooping_carts.user_id;
