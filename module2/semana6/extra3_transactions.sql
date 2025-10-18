BEGIN TRANSACTION;

-- Check if customer exists
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'ERROR: Customer C001 AND C002 does not exist'
        ELSE 'Customer found'
    END as customer_check,
    COUNT(*) as customer_count
FROM customers 
WHERE customer_id in ('C001','C002');

-- 1. Validar el stock
SELECT 
    COUNT(*) as product_available,
    CASE 
        WHEN COUNT(*) = 0 THEN 'ERROR: Product(s) do not exist'
        ELSE 'Product exists'
    END as product_check
FROM products 
WHERE product_id = 'P005';

-- 2. Capture initial inventory state with last_modified timestamp
CREATE TEMP TABLE initial_inventory_state AS
SELECT 
    product_id,
    quantity,
    last_modified,
    datetime('now') as snapshot_time
FROM inventory 
WHERE product_id = 'P005';

-- Show captured state
SELECT 
    product_id,
    quantity,
    last_modified as captured_last_modified,
    snapshot_time,
    CASE 
        WHEN quantity IS NULL THEN 'ERROR: No inventory record for products'
        WHEN quantity < 1 THEN 'ERROR: Insufficient stock for products'
        ELSE 'Stock available'
    END as inventory_check
FROM initial_inventory_state;

-- 3. Debug: Check all conditions before order creation
SELECT 
    'Debug - Order Creation Conditions:' as debug_info,
    CASE WHEN EXISTS (SELECT 1 FROM orders WHERE order_id = 'O004') 
         THEN 'FAIL: Order already exists' 
         ELSE 'PASS: Order does not exist' END as order_exists_check,
    CASE WHEN EXISTS (SELECT 1 FROM customers WHERE customer_id = 'C001') 
         THEN 'PASS: Customer exists' 
         ELSE 'FAIL: Customer does not exist' END as customer_exists_check,
    CASE WHEN EXISTS (SELECT 1 FROM inventory WHERE product_id = 'P005' AND quantity >= 1) 
         THEN 'PASS: Sufficient inventory' 
         ELSE 'FAIL: Insufficient inventory' END as inventory_sufficient_check,
    CASE WHEN EXISTS (
        SELECT 1 FROM inventory i
        JOIN initial_inventory_state iis ON i.product_id = iis.product_id
        WHERE i.product_id = 'P005' AND i.last_modified = iis.last_modified
    ) THEN 'PASS: Timestamps match' 
      ELSE 'FAIL: Timestamps do not match' END as timestamp_check;

-- 4. Before making any changes, verify the inventory hasn't been modified by another transaction
SELECT 
    CASE 
        WHEN i.last_modified = iis.last_modified THEN 'OK: Inventory unchanged'
        ELSE 'ERROR: Inventory was modified by another transaction'
    END as concurrency_check,
    i.last_modified as current_last_modified,
    iis.last_modified as captured_last_modified,
    i.quantity as current_quantity,
    iis.quantity as captured_quantity
FROM inventory i
JOIN initial_inventory_state iis ON i.product_id = iis.product_id
WHERE i.product_id = 'P005';

-- 5. Create first order with simplified conditions (step by step validation)
INSERT INTO orders (order_id, customer_id, total, status)
SELECT 'O004', 'C001', 100.00, 'Pending'
WHERE NOT EXISTS (SELECT 1 FROM orders WHERE order_id = 'O004')
AND EXISTS (SELECT 1 FROM customers WHERE customer_id = 'C001')
AND EXISTS (SELECT 1 FROM products WHERE product_id = 'P005')
AND EXISTS (
    SELECT 1 FROM inventory i
    WHERE i.product_id = 'P005' 
    AND i.quantity >= 1
    AND i.last_modified = (SELECT last_modified FROM initial_inventory_state WHERE product_id = 'P005')
);

-- Add shipping order status
INSERT INTO shipping_orders (order_id, product_id, customer_address, status)
SELECT 'O004', 'P005', 'MI, FL, 456 Wall St', 'Pending'
WHERE EXISTS (SELECT 1 FROM orders WHERE order_id = 'O004');

-- 5a. Check if order was created
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN 'SUCCESS: Order O004 was created'
        ELSE 'ERROR: Order O004 was NOT created'
    END as order_creation_status
FROM orders 
WHERE order_id = 'O004';

-- 6. Update inventory with optimistic locking for first order (only if order exists)
UPDATE inventory
SET 
    quantity = quantity - 1,
    last_modified = datetime('now')
WHERE product_id = 'P005'
AND last_modified = (SELECT last_modified FROM initial_inventory_state WHERE product_id = 'P005')
AND quantity >= 1
AND EXISTS (SELECT 1 FROM orders WHERE order_id = 'O004');

-- 7. Verify the first update was successful
SELECT 
    CASE 
        WHEN changes() > 0 THEN 'SUCCESS: First inventory update successful'
        ELSE 'ERROR: First inventory update failed - possible concurrent modification'
    END as first_update_result,
    changes() as rows_affected;

-- 8. Attempt to create second order for different customer (this should fail due to changed last_modified)
INSERT INTO orders (order_id, customer_id, total, status)
SELECT 'O005', 'C002', 100.00, 'Pending'
WHERE NOT EXISTS (SELECT 1 FROM orders WHERE order_id = 'O005')
AND EXISTS (SELECT 1 FROM customers WHERE customer_id = 'C002')
AND EXISTS (SELECT 1 FROM products WHERE product_id = 'P005')
AND EXISTS (
    SELECT 1 FROM inventory i
    WHERE i.product_id = 'P005' 
    AND i.quantity >= 1
    AND i.last_modified = (SELECT last_modified FROM initial_inventory_state WHERE product_id = 'P005')
);

-- 9. Check if second order was created (should be NO)
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN 'UNEXPECTED: Second order was created'
        ELSE 'EXPECTED: Second order was NOT created due to last_modified change'
    END as second_order_check
FROM orders 
WHERE order_id = 'O005';

-- 10. Show current inventory state vs original
SELECT 
    'Inventory Comparison:' as comparison,
    i.product_id,
    iis.quantity as original_quantity,
    i.quantity as current_quantity,
    iis.last_modified as original_last_modified,
    i.last_modified as current_last_modified,
    CASE 
        WHEN i.last_modified = iis.last_modified THEN 'SAME'
        ELSE 'CHANGED'
    END as timestamp_status
FROM inventory i
JOIN initial_inventory_state iis ON i.product_id = iis.product_id
WHERE i.product_id = 'P005';

-- 11. Final verification - show what orders were actually created
SELECT 
    'Final Status:' as status,
    COALESCE(o.order_id, 'NO ORDER') as order_id,
    COALESCE(o.customer_id, 'N/A') as customer_id,
    COALESCE(o.status, 'N/A') as order_status
FROM orders o
WHERE o.order_id IN ('O004', 'O005')
UNION ALL
SELECT 'Summary:', 
       CAST(COUNT(*) AS TEXT) || ' orders created', 
       '', ''
FROM orders 
WHERE order_id IN ('O004', 'O005');

-- Clean up temp table
DROP TABLE initial_inventory_state;

COMMIT;