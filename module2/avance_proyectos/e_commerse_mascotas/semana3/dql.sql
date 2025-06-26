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

SELECT * FROM sizes;
SELECT * FROM breeds;
SELECT * FROM stores;
SELECT * FROM users;
SELECT * FROM roles;
SELECT * FROM user_registrations;
SELECT * FROM products;
SELECT * FROM inventory;
SELECT * FROM product_registrations;
SELECT * FROM receipts;
SELECT * FROM sales;
SELECT * FROM shooping_carts;
SELECT * FROM shoopping_cart_items;

/*
THIS QUERY WILL GIVE YOU INFORMATION FOR THE FOLLOWING TABLES
  shooping_carts
  stores
*/

SELECT
    stores.name AS store_name,
    stores.email AS store_email,
    shooping_carts.user_email AS user_email,
    shooping_carts.status AS status,
    receipts.total_amount
FROM receipts
INNER JOIN stores ON receipts.store_id = stores.id
INNER JOIN shooping_carts ON receipts.cart_id = shooping_carts.id;


/*
THIS QUERY WILL GIVE YOU THE TOTAL AMOUNT FROM INFORMATION FOR THE FOLLOWING TABLES
  sales
  stores
  products
  receipts
*/

SELECT
    sales.receipt_id,
    sales.product_id,
    products.name AS name,
    sales.quantity,
    sales.price,
    sales.total_price
FROM sales
INNER JOIN products ON sales.product_id = products.id;

