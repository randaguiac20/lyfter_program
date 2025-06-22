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
SELECT * FROM users;
SELECT * FROM employees;
SELECT * FROM products;
SELECT * FROM product_receipts;
SELECT * FROM carts;
SELECT * FROM receipts;

/*1. Obtenga todos los productos almacenados*/
SELECT * FROM products;
/*2. Obtenga todos los productos que tengan 
     un precio mayor a 50000*/
SELECT * FROM products WHERE price > 50000;
/*3. Obtenga todas las compras de un mismo producto por id.*/
SELECT
    receipts.id AS receipt_id,
    receipts.receipt_number,
    product_receipts.product_id as product_id_from_product_receipts,
    products.id AS product_id_from_products
FROM receipts
INNER JOIN carts ON receipts.cart_id = carts.id
INNER JOIN product_receipts ON product_receipts.cart_id = carts.id
INNER JOIN products ON products.id = product_receipts.product_id
WHERE products.id = 2;

/*4. Obtenga todas las compras agrupadas por producto, donde
     se muestre el total comprado entre todas las compras.*/
SELECT
    SUM(receipts.total_amount) AS grand_total_amount
FROM receipts
INNER JOIN carts ON receipts.cart_id = carts.id
INNER JOIN product_receipts ON product_receipts.cart_id = carts.id
INNER JOIN products ON products.id = product_receipts.product_id
ORDER BY products.id;
/*5. Obtenga todas las facturas realizadas por el mismo comprador*/
SELECT
    receipts.receipt_number,
    users.name AS user_name,
    users.last_name AS user_lastname
FROM receipts
INNER JOIN carts ON receipts.cart_id = carts.id
INNER JOIN users ON carts.user_id = users.id
WHERE users.id = 1;
/*6. Obtenga todas las facturas ordenadas por monto total
     de forma descendente*/
SELECT * FROM receipts
ORDER BY total_amount;
/*7. Obtenga una sola factura por número de factura.*/
SELECT * FROM receipts WHERE receipt_number == 'RECP_0345';