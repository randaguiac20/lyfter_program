
SELECT * FROM customers;
SELECT * FROM customer_addresses;
SELECT * FROM products;
SELECT * FROM orders;
SELECT * FROM order_products;
SELECT
  o.id AS order_id,
  c.name AS customer_name,
  ca.address,
  p.name AS product_name,
  op.quantity,
  p.price,
  (op.quantity * p.price) AS total_item_price,
  o.delivery_time
FROM orders o
JOIN customers c ON o.customer_id = c.id
JOIN customer_addresses ca ON o.customer_address_id = ca.id
JOIN order_products op ON o.id = op.order_id
JOIN products p ON op.product_id = p.id;
