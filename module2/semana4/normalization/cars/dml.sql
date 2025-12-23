INSERT INTO owners (name, phone_number)
	VALUES ('Alice', '123-456-7890'),
           ('Bob', '987-654-3210'),
           ('Claire', '555-123-4567'),
           ('Dave', '111-222-3333');

INSERT INTO insurance_companies (name, policy)
	VALUES ('ABC Insurance', 'POL12345'),
           ('XYZ Insurance', 'POL54321'),
           ('DEF Insurance', 'POL67890'),
           ('GHI Insurance', 'POL98765');

INSERT INTO car_models (name)
	VALUES ('Accord'),
           ('CR-V'),
           ('Chevrolet');

INSERT INTO car_colors (name)
	VALUES ('sylver'),
           ('blue'),
           ('red');

INSERT INTO car_makers (name, model_id)
	VALUES ('Honda', 1),
           ('Honda', 1),
           ('Honda', 2),
           ('Chevrolet', 3);

INSERT INTO cars (owner_id, vin, maker_id,
                        color_id, year, insurance_id)
	VALUES (1, '1HGCM82633A', 1, 1, 2003, 1),
           (2, '1HGCM82633A', 1, 1, 2003, 2),
           (3, '5J6RM4H79EL', 2, 2, 2014, 3),
           (4, '1G1RA6EH1FU', 3, 3, 2015, 4);