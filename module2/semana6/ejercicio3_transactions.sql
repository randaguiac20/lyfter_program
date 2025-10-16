BEGIN TRANSACTION;

-- Check if order already exists
-- Actualizar el stock
UPDATE inventory
SET quantity = quantity + 1
WHERE product_id = 'P001'
AND EXISTS (
    SELECT 1 FROM orders 
    WHERE order_id = 'O001' 
    AND status = 'pending'
);

-- Actualizar factura
UPDATE orders
SET status = 'returned'
WHERE order_id = 'O001';

-- If there are any critical errors, rollback to savepoint
-- This would typically be handled by application logic
-- SELECT CASE WHEN final_status LIKE 'ERROR%' THEN ROLLBACK TO order_created END;

-- Si todo tuvo éxito, confirmamos los cambios.
COMMIT;