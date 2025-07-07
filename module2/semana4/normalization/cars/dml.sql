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

INSERT INTO car_models (name, vin)
	VALUES ('Accord', '1HGCM82633A'),
           ('CR-V', '5J6RM4H79EL'),
           ('Chevrolet', '1G1RA6EH1FU');

INSERT INTO car_colors (name)
	VALUES ('sylver'),
           ('blue'),
           ('red');

INSERT INTO car_makers (name)
	VALUES ('Honda'),
           ('Chevrolet');

INSERT INTO maker_models (model_id, maker_id)
	VALUES (1, 1),
           (2, 1),
           (3, 2);

INSERT INTO car_owners (owner_id, maker_model_id,
                        color_id, year, insurance_id)
	VALUES (1, 1, 1, 2003, 1),
           (2, 1, 1, 2003, 2),
           (3, 2, 2, 2014, 3),
           (4, 3, 3, 2015, 4);