BEGIN TRANSACTION;

-- Check if order already exists
-- Actualizar el stock
UPDATE inventory
SET quantity = quantity + 1
WHERE product_id = 'P001'
AND EXISTS (
    SELECT 1 FROM orders 
    WHERE order_id = 'O001'
    AND status = 'Pending'
);

-- Actualizar factura
UPDATE orders
SET status = 'Returned'
WHERE order_id = 'O001';

-- Si todo tuvo éxito, confirmamos los cambios.
COMMIT;