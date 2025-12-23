BEGIN TRANSACTION;

-- Check if customer exists
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'ERROR: Customer C002 does not exist'
        ELSE 'Customer found'
    END as customer_check,
    COUNT(*) as customer_count
FROM customers 
WHERE customer_id = 'C002';

-- 1. Validar el stock
SELECT 
    COUNT(*) as product_available,
    CASE 
        WHEN COUNT(*) = 0 THEN 'ERROR: Product(s) do not exist'
        ELSE 'Product exists'
    END as product_check
FROM products 
WHERE product_id IN ('P001', 'P003', 'P004');

-- Check inventory availability
SELECT 
    quantity,
    CASE 
        WHEN quantity IS NULL THEN 'ERROR: No inventory record for products'
        WHEN quantity < 4 THEN 'ERROR: Insufficient stock for products'
        ELSE 'Stock available'
    END as inventory_check
FROM inventory 
WHERE product_id = 'P001';

SELECT 
    quantity,
    CASE 
        WHEN quantity IS NULL THEN 'ERROR: No inventory record for products'
        WHEN quantity < 2 THEN 'ERROR: Insufficient stock for products'
        ELSE 'Stock available'
    END as inventory_check
FROM inventory 
WHERE product_id = 'P003';

SELECT 
    quantity,
    CASE 
        WHEN quantity IS NULL THEN 'ERROR: No inventory record for products'
        WHEN quantity < 6 THEN 'ERROR: Insufficient stock for products'
        ELSE 'Stock available'
    END as inventory_check
FROM inventory 
WHERE product_id = 'P004';

-- Only proceed if all validations pass
-- In a real implementation, you'd use conditional logic or stored procedures

-- 2. Si sí existe, crear la orden (only if it doesn't already exist)
INSERT INTO orders (order_id, customer_id, total, status)
SELECT 'O002', 'C002', 830.00, 'Pending'
WHERE NOT EXISTS (
    SELECT 1 FROM orders WHERE order_id = 'O002'
)
AND EXISTS (
    SELECT 1 FROM customers WHERE customer_id = 'C002'
);

-- 3. Add shipping order status
INSERT INTO shipping_orders (order_id, product_id, customer_address, status)
SELECT * FROM (
    SELECT 'O002' as order_id, 'P001' as product_id, 'MI, FL, 456 Wall St' as customer_address, 'Pending' as status
    UNION ALL
    SELECT 'O002', 'P003', 'MI, FL, 456 Wall St', 'Pending'
    UNION ALL
    SELECT 'O002', 'P004', 'MI, FL, 456 Wall St', 'Pending'
) AS order_data
WHERE EXISTS (SELECT 1 FROM orders WHERE order_id = 'O002');

-- Savepoint después de crear la orden
SAVEPOINT order_created;

-- Check if order was actually created
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN 'SUCCESS: Order created successfully'
        ELSE 'ERROR: Order was not created due to validation failures'
    END as order_creation_result
FROM orders 
WHERE order_id = 'O002';

-- 4. Actualizar el stock (only if order was created)
UPDATE inventory
SET quantity = quantity - 4
WHERE product_id = 'P001'
AND EXISTS (
    SELECT 1 FROM orders
    WHERE order_id = 'O002'
    AND status = 'Pending'    
);

UPDATE inventory
SET quantity = quantity - 2
WHERE product_id = 'P003'
AND EXISTS (
    SELECT 1 FROM orders
    WHERE order_id = 'O002'
    AND status = 'Pending'    
);

UPDATE inventory
SET quantity = quantity - 6
WHERE product_id = 'P004'
AND EXISTS (
    SELECT 1 FROM orders
    WHERE order_id = 'O002'
    AND status = 'Pending'    
);

-- Actualizar factura
UPDATE orders
SET status = 'Canceled'
WHERE order_id = 'O002' AND status = 'Pending';

-- Si todo tuvo éxito, confirmamos los cambios.
COMMIT;