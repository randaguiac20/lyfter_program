/*
Insert all the data for each table
Examples:
# INSERT
INSERT INTO students (name, last_name, spanish_score)
	VALUES ('Alek', 'Castillo', 56);
# INSERT
INSERT INTO RealTimeData (data_data_name, data_value) 
VALUES ('Temperature', '25.6'),
       (2, 'Humidity', '60%'),
       (3, 'Pressure', '1013.25'),
       (4, 'Wind Speed', '12.5');
INSERT INTO students (name, last_name, english_score, spanish_score)
	VALUES ('Juan', 'Lopez', 100, 100);
	
INSERT INTO students (name, last_name)
	VALUES ('Sam', 'Fisher');
# UPDATE
UPDATE students SET
	last_name = 'Castillo Bogantes',
	english_score = 97
WHERE id = 1;
UPDATE students SET
	last_name = 'Garcia'
WHERE id = 2;
# DELETE
DELETE FROM students
	WHERE id = 3;
*/

INSERT INTO breeds (name, description, size)
	VALUES 
    ('chiguagua', 'Energetic and noise dog', 'small'),
    ('golden', 'Energetic and friendly dog', 'medium'),
    ('boxer', 'Medium energy and guard dog', 'medium'),
    ('doberman', 'Very smart, friendly and guard dog', 'large');

INSERT INTO roles (name, description)
	VALUES 
    ('administrator', 'Full access priviledges for everything'),
    ('client', 'Read Only access'),
    ('developer', 'Read and write access to development only');


INSERT INTO users (name, lastname, email, description, role_id, status)
	VALUES 
    ('Ronaldo', 'DeLima', 'r9delima@gmail.com', 'Very fast and gifted soccer player', 1, 'active'),
    ('Roger', 'Federer', 'rfederer@gmail.com',  'Amazing tennis player', 2, 'active'),
    ('Stephen', 'Curry', 'scurry@gmail.com',  'One of a kind basketball player', 3, 'active');

INSERT INTO products (sku, name, size, breed_size_id, description,
                      quantity, price, brand, ingress_date, expiration_date, status)
	VALUES 
    ('sku123', 'Bully Sticks', 'medium', 1, 'Make of cow', 45, 2450.00, 'New Valley', '2025-06-23', '2025-06-23', 'active'),
    ('sku456', 'Salmon Treats', 'small', 1, 'Europe Salmon Treats', 67, 5890.00, 'Organic Foods', '2025-06-23', '2025-06-23', 'active'),
    ('sku789', 'Chicken Cookies', 'medium', 3, 'Tasty chicken cookies', 39, 3548.00, 'Nutrisource', '2025-06-23', '2025-06-23', 'active');

INSERT INTO shooping_carts (user_id, status, purchase_date)
	VALUES 
    (1, 'finished', '2025-06-23'),
    (3, 'finished', '2025-06-23');

INSERT INTO shoopping_cart_products (cart_id, product_id, quantity, checkout)
	VALUES 
    (1, 3, 2, 1),
    (1, 2, 5, 1),
    (1, 1, 3, 1);

INSERT INTO shoopping_cart_products (cart_id, product_id, quantity, checkout)
	VALUES 
    (2, 1, 1, 1),
    (2, 2, 3, 1),
    (2, 3, 2, 1);

INSERT INTO receipts (cart_id, description,
                      payment_method, total_amount, purchase_date)
	VALUES 
    (1, 'Dog treats', 'credit card', 43896.0, '2025-06-23'),
    (2, 'Dog treats', 'debit card', 27216.0, '2025-06-23');

