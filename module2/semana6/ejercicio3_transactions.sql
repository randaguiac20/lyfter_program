BEGIN TRANSACTION;

-- Check if order already exists
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN 'ERROR: Order O001 already exists'
        ELSE 'Order ID available'
    END as order_check,
    COUNT(*) as existing_orders
FROM orders 
WHERE order_id = 'O001';

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

-- Check if order was actually created
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN 'SUCCESS: Order created successfully'
        ELSE 'ERROR: Order was not created due to validation failures'
    END as order_creation_result
FROM orders 
WHERE order_id = 'O001';

-- Actualizar el stock
UPDATE inventory
SET quantity = quantity + 1
WHERE product_id = 'P001'
AND EXISTS (SELECT 1 FROM orders WHERE order_id = 'O001');

-- Actualizar factura
UPDATE orders
SET status = 'returned'
WHERE order_id = 'O001';

-- If there are any critical errors, rollback to savepoint
-- This would typically be handled by application logic
-- SELECT CASE WHEN final_status LIKE 'ERROR%' THEN ROLLBACK TO order_created END;

-- Si todo tuvo éxito, confirmamos los cambios.
COMMIT;