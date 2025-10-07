BEGIN TRANSACTION;

-- 1. Validar el stock
SELECT COUNT(*) as product_available
FROM products 
WHERE product_id = 'P001';

-- 2. Si sí existe, crear la orden
INSERT INTO orders (order_id, customer_id, total, status)
VALUES ('O001', 'C001', 100.00, 'Pending');

-- 3. Actualizar el stock
UPDATE inventory
SET quantity = quantity - 1
WHERE product_id = 'P001';

-- Savepoint después de crear la orden
SAVEPOINT order_created;
-- Para este punto la orden fue creada y el stock actualizado. 
-- Es un buen momento para crear un savepoint.

-- 4. Generar el envío
INSERT INTO shipping (order_id, address, status)
VALUES ('O001', '123 Main St', 'Pending');

-- 5. Actualizar la ultima compra del usuario
UPDATE customers
SET last_purchase = CURRENT_DATE
WHERE customer_id = 'C001';

-- Validamos que la orden se haya creado correctamente
SELECT * FROM shipping;
-- Check for various "empty" conditions
SELECT 
    address,
    CASE 
        WHEN address IS NULL THEN 'WARNING: Address is NULL'
        WHEN address = '' THEN 'WARNING: Address is empty string'
        WHEN trim(address) = '' THEN 'WARNING: Address is only whitespace'
        ELSE ROLLBACK TO order_created;
    END as address_check
FROM shipping 
WHERE order_id = 'O001';

-- Si todo tuvo éxito, confirmamos los cambios.
COMMIT;