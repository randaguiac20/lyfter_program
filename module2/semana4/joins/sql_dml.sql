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


>>> DML = Definition Manipulation Language
*/


INSERT INTO books (name, author_id)
	VALUES ('Don Quijote', 1),
           ('La Divina Comedia', 2),
           ('Vagabond 1-3', 3),
           ('Dragon Ball 1', 4),
           ('The Book of the 5 Rings', NULL);

INSERT INTO authors (name)
	VALUES ('Miguel de Cervantes'),
           ('Dante Alighieri'),
           ('Takehiko Inoue'),
           ('Akira Toriyama'),
           ('Walt Disney');

INSERT INTO customers (name, email)
	VALUES ('John Doe', 'j.doe@email.com'),
           ('Jane Doe', 'jane@doe.com'),
           ('Luke Skywalker', 'darth.son@email.com');

INSERT INTO rents (book_id, customer_id, state)
	VALUES (1, 2, 'Returned'),
           (2, 2, 'Returned'),
           (1, 1, 'On time'),
           (3, 1, 'On time'),
           (2, 2, 'Overdue');
