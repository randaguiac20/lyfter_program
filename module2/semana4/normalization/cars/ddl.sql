
DROP TABLE owners;
DROP TABLE insurance_companies;
DROP TABLE car_colors;
DROP TABLE car_models;
DROP TABLE car_makers;
DROP TABLE cars;



CREATE TABLE owners (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL,
	phone_number VARCHAR(50) NOT NULL
);

CREATE TABLE insurance_companies (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name VARCHAR(50) NOT NULL,
	policy VARCHAR(50) NOT NULL
);

CREATE TABLE car_models (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE car_colors (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE car_makers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
	model_id INT NOT NULL,
	FOREIGN KEY(model_id) REFERENCES car_models(id)
);

CREATE TABLE cars (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INT NOT NULL,
	vin VARCHAR(50) NOT NULL,
	maker_id INT NOT NULL,
	color_id INT NOT NULL,
    year INT NOT NULL,
	insurance_id INT NOT NULL,
	FOREIGN KEY(owner_id) REFERENCES owners(id),
	FOREIGN KEY(maker_id) REFERENCES maker_models(id),
	FOREIGN KEY(color_id) REFERENCES car_colors(id),
    FOREIGN KEY(insurance_id) REFERENCES insurance_companies(id)
);