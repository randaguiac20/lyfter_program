BEGIN TRANSACTION;

-- Check if customer exists
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'ERROR: Customer C001 does not exist'
        ELSE 'Customer found'
    END as customer_check,
    COUNT(*) as customer_count
FROM customers 
WHERE customer_id = 'C001';

-- 1. Validar el stock
SELECT 
    COUNT(*) as product_available,
    CASE 
        WHEN COUNT(*) = 0 THEN 'ERROR: Product P001 does not exist'
        ELSE 'Product exists'
    END as product_check
FROM products 
WHERE product_id = 'P001';

-- Check inventory availability
SELECT 
    quantity,
    CASE 
        WHEN quantity IS NULL THEN 'ERROR: No inventory record for product P001'
        WHEN quantity < 1 THEN 'ERROR: Insufficient stock for product P001'
        ELSE 'Stock available'
    END as inventory_check
FROM inventory 
WHERE product_id = 'P001';

-- Only proceed if all validations pass
-- In a real implementation, you'd use conditional logic or stored procedures

-- 2. Si sí existe, crear la orden (only if it doesn't already exist)
INSERT INTO orders (order_id, customer_id, total, status)
SELECT 'O001', 'C001', 100.00, 'Pending'
WHERE NOT EXISTS (
    SELECT 1 FROM orders WHERE order_id = 'O001'
)
AND EXISTS (
    SELECT 1 FROM customers WHERE customer_id = 'C001'
)
AND EXISTS (
    SELECT 1 FROM products WHERE product_id = 'P001'
)
AND EXISTS (
    SELECT 1 FROM inventory WHERE product_id = 'P001' AND quantity >= 1
);

-- Check if order was actually created
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN 'SUCCESS: Order created successfully'
        ELSE 'ERROR: Order was not created due to validation failures'
    END as order_creation_result
FROM orders 
WHERE order_id = 'O001';

-- 3. Actualizar el stock (only if order was created)
UPDATE inventory
SET quantity = quantity - 1
WHERE product_id = 'P001'
AND EXISTS (SELECT 1 FROM orders WHERE order_id = 'O001');

-- Savepoint después de crear la orden
SAVEPOINT order_created;

-- 4. Generar el envío (check if shipping record already exists)
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN 'WARNING: Shipping record for order O001 already exists'
        ELSE 'No existing shipping record found'
    END as shipping_check
FROM shipping_orders 
WHERE order_id = 'O001';

INSERT INTO shipping_orders (order_id, product_id, customer_address, status)
SELECT 'O001', 'P001', '123 Main St', 'Pending'
WHERE NOT EXISTS (
    SELECT 1 FROM shipping_orders WHERE order_id = 'O001'
)
AND EXISTS (
    SELECT 1 FROM orders WHERE order_id = 'O001'
);

-- 5. Actualizar la ultima compra del usuario
UPDATE customers
SET last_purchase = CURRENT_DATE
WHERE customer_id = 'C001'
AND EXISTS (SELECT 1 FROM orders WHERE order_id = 'O001');

-- Final validation of the complete transaction
SELECT 
    o.order_id,
    o.status as order_status,
    c.address as customer_address,
    s.status as shipping_status,
    i.quantity as remaining_stock,
    c.last_purchase,
    CASE 
        WHEN s.customer_address IS NULL THEN 'ERROR: Address is NULL'
        WHEN s.customer_address = '' THEN 'ERROR: Address is empty string'
        WHEN trim(s.customer_address) = '' THEN 'ERROR: Address is only whitespace'
        ELSE 'SUCCESS: Transaction completed successfully'
    END as final_status
FROM orders o
LEFT JOIN shipping_orders s ON o.order_id = s.order_id
LEFT JOIN inventory i ON i.product_id = 'P001'
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_id = 'O001';

-- If there are any critical errors, rollback to savepoint
-- This would typically be handled by application logic
-- SELECT CASE WHEN final_status LIKE 'ERROR%' THEN ROLLBACK TO order_created END;

-- Si todo tuvo éxito, confirmamos los cambios.
COMMIT;