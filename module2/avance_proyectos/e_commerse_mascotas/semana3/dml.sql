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

INSERT INTO stores (name, description, email)
	VALUES 
    ('Pet Kiras Store', 'Chicago store', 'pets_kiras_chicago@gmail.com'),
    ('Pet Klays Store', 'Atlanta store', 'pets_klays_atlanta@gmail.com');

INSERT INTO sizes (size, description)
	VALUES 
    ('small', 'Small size'),
    ('medium', 'Medium size'),
    ('large', 'Large size'),
    ('extra-large', 'Extra large size');

INSERT INTO breeds (name, description, size_id)
	VALUES 
    ('chiguagua', 'Energetic and noise dog', 1),
    ('golden', 'Energetic and friendly dog', 3),
    ('boxer', 'Medium energy and guard dog', 2),
    ('doberman', 'Very smart, friendly and guard dog', 3);

INSERT INTO roles (name, description)
	VALUES 
    ('administrator', 'Full access priviledges for everything'),
    ('client', 'Read Only access'),
    ('developer', 'Read and write access to development only');


INSERT INTO users (name, lastname, email, description)
	VALUES 
    ('Ronaldo', 'DeLima', 'r9delima@gmail.com', 'Very fast and gifted soccer player'),
    ('Roger', 'Federer', 'rfederer@gmail.com',  'Amazing tennis player'),
    ('Stephen', 'Curry', 'scurry@gmail.com',  'One of a kind basketball player');

INSERT INTO user_registrations (user_id, role_id, status)
	VALUES 
    (1, 1, 'active'),
    (3, 2, 'disable'),
    (2, 3, 'active');

INSERT INTO products (sku, name, size_id, breed_size_id, description, price, brand, expiration_date)
	VALUES 
    ('sku123', 'Bully Sticks', 2, 1, 'Make of cow', 2450.00, 'New Valley', '2025-06-23'),
    ('sku456', 'Salmon Treats', 1, 1, 'Europe Salmon Treats', 5890.00, 'Organic Foods', '2025-06-23'),
    ('sku789', 'Chicken Cookies', 3, 3, 'Tasty chicken cookies', 3548.00, 'Nutrisource', '2025-06-23');

INSERT INTO product_registrations (product_id, inventory_id, description, ingress_date)
	VALUES 
    (1, 1, 'New product', '2025-06-23'),
    (2, 2, 'New product', '2025-06-23'),
    (3, 3, 'New product', '2025-06-23');

INSERT INTO inventory (product_id, description, quantity, status)
	VALUES 
    (1, 'New product', 45, 'active'),
    (2, 'New product', 56, 'active'),
    (3, 'New product', 34, 'active');

INSERT INTO shooping_carts (user_id, user_email, status, purchase_date)
	VALUES 
    (1, 'r9delima@gmail.com', 'finished', '2025-06-23'),
    (3, 'scurry@gmail.com', 'finished', '2025-06-23');

INSERT INTO shoopping_cart_items (cart_id, product_id, quantity, price)
	VALUES 
    (1, 3, 2, 3548.00),
    (1, 2, 5, 5890.00),
    (1, 1, 3, 2450.00);

INSERT INTO shoopping_cart_items (cart_id, product_id, quantity, price)
	VALUES 
    (2, 1, 1, 2450.00),
    (2, 2, 3, 5890.00),
    (2, 3, 2, 3548.00);

INSERT INTO receipts (user_id, cart_id, store_id, description,
                      payment_method, total_amount, purchase_date)
	VALUES 
    (1, 1, 1,'Dog treats', 'credit card', 43896.0, '2025-06-23'),
    (3, 2, 2,'Dog treats', 'debit card', 27216.0, '2025-06-23');

INSERT INTO sales (receipt_id, product_id, quantity, price,
                   total_price)
	VALUES 
    (1, 3, 2, 3548.00, 7096.00),
    (1, 2, 5, 5890.00, 29450.00),
    (1, 1, 3, 2450.00, 7350.00),
    (2, 1, 1, 2450.00, 2450.00),
    (2, 2, 3, 5890.00, 17670.00),
    (2, 3, 2, 3548.00, 7096.00);
