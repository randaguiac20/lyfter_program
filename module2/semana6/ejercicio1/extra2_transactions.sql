-- DISCLAIMER
-- THIS ONE I DID NOT DO IT BY MY OWN, I MADE USE OF AI TO GET IT DONE
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

-- 1. Create a table with available products only
CREATE TEMP TABLE available_products AS
SELECT 
    p.product_id,
    i.quantity,
    CASE 
        WHEN p.product_id = 'P001' AND i.quantity >= 4 THEN 4
        WHEN p.product_id = 'P003' AND i.quantity >= 2 THEN 2
        WHEN p.product_id = 'P004' AND i.quantity >= 6 THEN 6
        ELSE 0
    END as required_quantity,
    CASE 
        WHEN p.product_id = 'P001' AND i.quantity >= 4 THEN 100.00
        WHEN p.product_id = 'P003' AND i.quantity >= 2 THEN 85.00
        WHEN p.product_id = 'P004' AND i.quantity >= 6 THEN 75.00
        ELSE 0
    END as unit_price
FROM products p
JOIN inventory i ON p.product_id = i.product_id
WHERE p.product_id IN ('P001', 'P003', 'P004')
AND (
    (p.product_id = 'P001' AND i.quantity >= 4) OR
    (p.product_id = 'P003' AND i.quantity >= 2) OR
    (p.product_id = 'P004' AND i.quantity >= 6)
);

-- Show which products are available
SELECT 
    product_id,
    quantity as current_stock,
    required_quantity,
    unit_price,
    'Available for order' as status
FROM available_products;

-- Show which products are NOT available
SELECT 
    p.product_id,
    COALESCE(i.quantity, 0) as current_stock,
    CASE 
        WHEN p.product_id = 'P001' THEN 4
        WHEN p.product_id = 'P003' THEN 2
        WHEN p.product_id = 'P004' THEN 6
    END as required_quantity,
    'Insufficient stock - NOT included in order' as status
FROM products p
LEFT JOIN inventory i ON p.product_id = i.product_id
WHERE p.product_id IN ('P001', 'P003', 'P004')
AND p.product_id NOT IN (SELECT product_id FROM available_products);

-- Calculate total for available products only
CREATE TEMP TABLE order_total AS
SELECT 
    COALESCE(SUM(required_quantity * unit_price), 0) as total_amount,
    COUNT(*) as products_count
FROM available_products;

-- Show order summary
SELECT 
    total_amount,
    products_count,
    CASE 
        WHEN products_count = 0 THEN 'No products available - Order will not be created'
        ELSE 'Order will be created with available products only'
    END as order_status
FROM order_total;

-- 2. Create order only if at least one product is available
INSERT INTO orders (order_id, customer_id, total, status)
SELECT 'O003', 'C002', ot.total_amount, 'Pending'
FROM order_total ot
WHERE NOT EXISTS (
    SELECT 1 FROM orders WHERE order_id = 'O003'
)
AND EXISTS (
    SELECT 1 FROM customers WHERE customer_id = 'C002'
)
AND ot.products_count > 0;  -- Only create if at least one product is available

-- 3. Add shipping orders only for available products (this serves as order details)
INSERT OR IGNORE INTO shipping_orders (order_id, product_id, customer_address, status)
SELECT 
    'O003' as order_id, 
    ap.product_id, 
    'MI, FL, 456 Wall St' as customer_address, 
    'Pending' as status
FROM available_products ap
WHERE EXISTS (SELECT 1 FROM orders WHERE order_id = 'O003');

-- Savepoint después de crear la orden
SAVEPOINT order_created;

-- Check if order was actually created
SELECT 
    CASE 
        WHEN COUNT(*) > 0 THEN 'SUCCESS: Order created with available products'
        ELSE 'ERROR: Order was not created - no products available'
    END as order_creation_result,
    COALESCE(total, 0) as final_total
FROM orders 
WHERE order_id = 'O003';

-- 4. Update inventory only for products that were actually ordered
UPDATE inventory
SET quantity = quantity - (
    SELECT required_quantity 
    FROM available_products 
    WHERE available_products.product_id = inventory.product_id
)
WHERE product_id IN (SELECT product_id FROM available_products)
AND EXISTS (
    SELECT 1 FROM orders
    WHERE order_id = 'O003'
    AND status = 'Pending'    
);

-- Final status
UPDATE orders
SET status = 'Confirmed'
WHERE order_id = 'O003' AND status = 'Pending';

-- Show final order details
SELECT 
    'Final Order Summary:' as summary,
    o.order_id,
    o.total,
    o.status,
    COUNT(so.product_id) as products_included
FROM orders o
LEFT JOIN shipping_orders so ON o.order_id = so.order_id
WHERE o.order_id = 'O003'
GROUP BY o.order_id, o.total, o.status;

-- Show detailed products in the order
SELECT 
    so.order_id,
    so.product_id,
    ap.required_quantity,
    ap.unit_price,
    (ap.required_quantity * ap.unit_price) as line_total
FROM shipping_orders so
JOIN available_products ap ON so.product_id = ap.product_id
WHERE so.order_id = 'O003';

-- Clean up temp tables
DROP TABLE available_products;
DROP TABLE order_total;

-- Si todo tuvo éxito, confirmamos los cambios.
COMMIT;
