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
    name VARCHAR(50) NOT NULL,
    vin VARCHAR(50) NOT NULL
);

CREATE TABLE car_colors (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE car_makers (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL
);

CREATE TABLE maker_models (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INT NOT NULL,
	maker_id INT NOT NULL,
	FOREIGN KEY(model_id) REFERENCES car_models(id),
	FOREIGN KEY(maker_id) REFERENCES car_makers(id)
);

CREATE TABLE car_owners (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
    owner_id INT NOT NULL,
	maker_model_id INT NOT NULL,
    color_id VARCHAR(50) NOT NULL,
    year INT NOT NULL,
	insurance_id INT NOT NULL,
	FOREIGN KEY(owner_id) REFERENCES owners(id),
    FOREIGN KEY(color_id) REFERENCES car_colors(id),
	FOREIGN KEY(maker_model_id) REFERENCES maker_models(id),
    FOREIGN KEY(insurance_id) REFERENCES insurance_companies(id)
);