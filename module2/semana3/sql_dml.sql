/*
Insert all the data for each table
Examples:

# INSERT
INSERT INTO students (id, name, last_name, spanish_score)
	VALUES (1, 'Alek', 'Castillo', 56);

# INSERT
INSERT INTO RealTimeData (data_id, data_name, data_value) 
VALUES (1, 'Temperature', '25.6'),
       (2, 'Humidity', '60%'),
       (3, 'Pressure', '1013.25'),
       (4, 'Wind Speed', '12.5');

INSERT INTO students (id, name, last_name, english_score, spanish_score)
	VALUES (1, 'Juan', 'Lopez', 100, 100);
	
INSERT INTO students (id, name, last_name, english_score, spanish_score, science_score)
	VALUES (1, 'Sam', 'Fisher', 100, 100, 60);

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
INSERT INTO users (name, last_name, phone_number, email)
	VALUES ('Alek', 'Castillo', '506-60457490', 'alekc@gmail.com'),
           ('Andre', 'Salmeron', '506-60457491', 'andres@gmail.com'),
           ('Rodrigo', 'Salas', '506-60457492', 'rodris@gmail.com'),
           ('Klay', 'Aguilar', '506-60457493', 'klaya@gmail.com'),
           ('Kira', 'Carrillo', '506-60457494', 'kirac@gmail.com');

INSERT INTO employees (code, role, name, last_name, phone_number, email)
	VALUES ('brianc', 'cashier','Brian', 'Castillo', '506-60457490', 'brianc@gmail.com'),
           ('joses', 'cashier','Jose', 'Salmeron', '506-60457491', 'joses@gmail.com'),
           ('ronaldon', 'cashier','Ronaldo', 'Nasario', '506-60457492', 'ronaldon@gmail.com'),
           ('stephenc', 'cashier','Stephen', 'Curry', '506-60457493', 'stephenc@gmail.com'),
           ('rogerf', 'cashier','Roger', 'Federer', '506-60457494', 'rogerf@gmail.com');

INSERT INTO products (code, name, brand, price)
	VALUES ('COD_012', 'bully sticks', 'organic products', 45000),
           ('COD_345', 'salmon treats', 'montebello', 36500),
           ('COD_678', 'chicken treats', 'organic products', 53450),
           ('COD_910', 'lamb treats', 'montebello', 64850),
           ('COD_911', 'chicken cookies', 'nutrisource', 50250);

INSERT INTO product_receipts (receipt_code, quantity, amount, taxes,
                              client_phone_number, employeed_code,
                              user_id, product_id, cart_id)
VALUES ('PRECP_0001', 5, 251250, 13, '506-60457490', 'ronaldon', 1, 5, 1),
       ('PRECP_0001', 3, 109500, 13, '506-60457490', 'ronaldon', 1, 2, 1),
       ('PRECP_0001', 2, 106900, 13, '506-60457490', 'ronaldon', 1, 3, 1),
       ('PRECP_0001', 1, 64850, 13, '506-60457490', 'ronaldon', 1, 4, 1),
       ('PRECP_0001', 2, 90000, 13, '506-60457490', 'ronaldon', 1, 1, 1);

INSERT INTO product_receipts (receipt_code, quantity, amount, taxes,
                              client_phone_number, employeed_code,
                              user_id, product_id, cart_id)
VALUES ('PRECP_0002', 5, 251250, 13, '506-60457494', 'stephenc', 4, 5, 2),
       ('PRECP_0002', 3, 109500, 13, '506-60457494', 'stephenc', 4, 2, 2),
       ('PRECP_0002', 2, 106900, 13, '506-60457494', 'stephenc', 4, 3, 2);

INSERT INTO product_receipts (receipt_code, quantity, amount, taxes,
                              client_phone_number, employeed_code,
                              user_id, product_id, cart_id)
VALUES ('PRECP_0003', 5, 251250, 13, '506-60457492', 'rogerf', 1, 5, 3),
       ('PRECP_0003', 1, 64850, 13, '506-60457492', 'rogerf', 1, 4, 3),
       ('PRECP_0003', 2, 90000, 13, '506-60457492', 'rogerf', 1, 1, 3);

INSERT INTO product_receipts (receipt_code, quantity, amount, taxes,
                              client_phone_number, employeed_code,
                              user_id, product_id, cart_id)
VALUES ('PRECP_0004', 1, 64850, 13, '506-60457490', 'ronaldon', 2, 4, 4),
       ('PRECP_0004', 2, 90000, 13, '506-60457490', 'ronaldon', 2, 1, 4);

INSERT INTO carts (user_id, product_receipt_code)
VALUES (1, 'PRECP_0001');

INSERT INTO carts (user_id, product_receipt_code)
VALUES (4, 'PRECP_0002');

INSERT INTO carts (user_id, product_receipt_code)
VALUES (1, 'PRECP_0003');

INSERT INTO carts (user_id, product_receipt_code)
VALUES (2, 'PRECP_0004');

INSERT INTO receipts (receipt_number, total_amount,
                      cart_id)
VALUES ('RECP_0123', 622500, 1);

INSERT INTO receipts (receipt_number, total_amount,
                      cart_id)
VALUES ('RECP_0345', 467650, 2);

INSERT INTO receipts (receipt_number, total_amount,
                      cart_id)
VALUES ('RECP_0678', 406100, 3);

INSERT INTO receipts (receipt_number, total_amount,
                      cart_id)
VALUES ('RECP_0910', 154850, 4);
