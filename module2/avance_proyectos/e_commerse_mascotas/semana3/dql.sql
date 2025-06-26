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
SELECT * FROM carts;

/*
THIS QUERY WILL GIVE YOU INFORMATION FOR THE FOLLOWING TABLES
  receipts
  carts
  sales
  users
  stores
*/

SELECT
    receipts.receipt_number AS receipt_number,
    sales.cart_reference_number AS cart_number,
    users.email AS user_email,
    stores.name AS store_name,
    stores.email AS store_email,
    products.name as product_name,
    products.price as price
FROM carts
INNER JOIN receipts ON sales.receipt_id = receipts.id
INNER JOIN sales ON sales.cart_reference_number = carts.reference_number
INNER JOIN users ON carts.user_id = users.id
INNER JOIN stores ON carts.store_id = stores.id
INNER JOIN products ON carts.store_id = products.id;


/*
THIS QUERY WILL GIVE YOU THE TOTAL AMOUNT FROM INFORMATION FOR THE FOLLOWING TABLES
  sales
  stores
  products
  receipts
*/

SELECT
    receipts.receipt_number AS receipt_number,
    sales.cart_reference_number AS cart_number,
    products.name as product_name,
    receipts.total_amount as total_amount
FROM carts
INNER JOIN receipts ON sales.receipt_id = receipts.id
INNER JOIN sales ON sales.cart_reference_number = carts.reference_number
INNER JOIN stores ON carts.store_id = stores.id
INNER JOIN products ON carts.store_id = products.id
WHERE receipt_number = 'REP0123'
GROUP BY receipt_number;

/*
THIS QUERY WILL GIVE YOU INFORMATION FOR THE FOLLOWING TABLES
  products
  inventory
  product_registrations
*/
SELECT
    pr.ingress_date,
    products.sku AS sku,
    products.name AS name,
    products.price AS price,
    products.brand AS brand_name,
    products.expiration_date AS expiration_date,
    inventory.quantity AS quantity,
    inventory.status AS status
FROM product_registrations AS pr
INNER JOIN products ON pr.product_id = products.id
INNER JOIN inventory ON pr.inventory_id = inventory.id;
