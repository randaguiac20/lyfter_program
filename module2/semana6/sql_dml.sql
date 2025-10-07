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
INSERT INTO customers (customer_id, name, last_name, address)
	VALUES ('C001', 'Alek', 'Castillo', '123 Main St');

INSERT INTO products (product_id, name, brand)
	VALUES ('P001', 'bully sticks', 'organic products'),
           ('P002', 'salmon treats', 'montebello');

INSERT INTO inventory (product_id, quantity)
	VALUES ('P001', 8),
           ('P002', 3);


