-- Create schema if needed (optional)
CREATE SCHEMA IF NOT EXISTS lyfter_car_rental AUTHORIZATION randall_aguilar;

-- Ensure subsequent objects are created only in this schema by default
SET search_path TO lyfter_car_rental;

CREATE TABLE IF NOT EXISTS lyfter_car_rental.users (
   id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
   first_name VARCHAR(255) NOT NULL,
   last_name VARCHAR(50) NOT NULL,
   email VARCHAR(254) UNIQUE NOT NULL CHECK (
      email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
   ),
   username VARCHAR(50) NOT NULL,
   password VARCHAR(50) NOT NULL,
   account_status VARCHAR(50) NOT NULL,
   birthday DATE NOT NULL,
   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO lyfter_car_rental.users (first_name, last_name, email, username, password, birthday, account_status) VALUES
('Sofía', 'Ramírez', 'sofia.ramirez@example.com', 'sramirez', 'p@55w0rd1!', '1991-07-15', 'active'),
('Mateo', 'López', 'mateo.lopez@example.com', 'mlopez', 'p@55w0rd2!', '1989-03-22', 'active'),
('Valentina', 'Hernández', 'valentina.hernandez@example.com', 'vhernandez', 'p@55w0rd3!', '1995-09-12', 'inactive'),
('Diego', 'Martínez', 'diego.martinez@example.com', 'dmartinez', 'p@55w0rd4!', '1990-01-08', 'active'),
('Camila', 'Gómez', 'camila.gomez@example.com', 'cgomez', 'p@55w0rd5!', '1993-04-05', 'suspended'),
('Emilia', 'Torres', 'emilia.torres@example.com', 'etorres', 'p@55w0rd6!', '1997-12-30', 'active'),
('Lucas', 'Silva', 'lucas.silva@example.com', 'lsilva', 'p@55w0rd7!', '1988-06-16', 'inactive'),
('Isabella', 'Díaz', 'isabella.diaz@example.com', 'idiaz', 'p@55w0rd8!', '1992-10-21', 'active'),
('Santiago', 'Morales', 'santiago.morales@example.com', 'smorales', 'p@55w0rd9!', '1985-11-19', 'suspended'),
('Regina', 'Rojas', 'regina.rojas@example.com', 'rrojas', 'p@55w0rd10!', '1994-08-25', 'active'),
('Sebastián', 'Mendoza', 'sebastian.mendoza@example.com', 'smendoza', 'p@55w0rd11!', '1990-02-14', 'active'),
('Mariana', 'Navarro', 'mariana.navarro@example.com', 'mnavarro', 'p@55w0rd12!', '1987-07-07', 'inactive'),
('Andrés', 'Santos', 'andres.santos@example.com', 'asantos', 'p@55w0rd13!', '1991-05-13', 'active'),
('Renata', 'Castillo', 'renata.castillo@example.com', 'rcastillo', 'p@55w0rd14!', '1996-10-02', 'suspended'),
('Tomás', 'Ortiz', 'tomas.ortiz@example.com', 'tortiz', 'p@55w0rd15!', '1986-01-17', 'active'),
('Daniela', 'Luna', 'daniela.luna@example.com', 'dluna', 'p@55w0rd16!', '1993-03-03', 'inactive'),
('Nicolás', 'Vargas', 'nicolas.vargas@example.com', 'nvargas', 'p@55w0rd17!', '1995-06-09', 'active'),
('Alexa', 'Guerrero', 'alexa.guerrero@example.com', 'aguerrero', 'p@55w0rd18!', '1992-11-11', 'active'),
('Iván', 'Camacho', 'ivan.camacho@example.com', 'icamacho', 'p@55w0rd19!', '1989-04-27', 'inactive'),
('Aitana', 'Peña', 'aitana.pena@example.com', 'apena', 'p@55w0rd20!', '1990-09-30', 'suspended'),
('Maximiliano', 'Salinas', 'max.salinas@example.com', 'msalinas', 'p@55w0rd21!', '1987-02-20', 'active'),
('Fernanda', 'Cabrera', 'fernanda.cabrera@example.com', 'fcabrera', 'p@55w0rd22!', '1996-12-12', 'active'),
('Julián', 'Mejía', 'julian.mejia@example.com', 'jmejia', 'p@55w0rd23!', '1993-06-04', 'inactive'),
('Andrea', 'Valdez', 'andrea.valdez@example.com', 'avaldez', 'p@55w0rd24!', '1988-03-26', 'active'),
('Emiliano', 'Escobar', 'emiliano.escobar@example.com', 'eescobar', 'p@55w0rd25!', '1994-07-01', 'suspended'),
('Montserrat', 'Miranda', 'montserrat.miranda@example.com', 'mmiranda', 'p@55w0rd26!', '1991-05-18', 'active'),
('Leonardo', 'Cortés', 'leonardo.cortes@example.com', 'lcortes', 'p@55w0rd27!', '1986-08-29', 'inactive'),
('Victoria', 'Ríos', 'victoria.rios@example.com', 'vrios', 'p@55w0rd28!', '1997-01-10', 'active'),
('Gabriel', 'Lara', 'gabriel.lara@example.com', 'glara', 'p@55w0rd29!', '1990-11-15', 'active'),
('Paula', 'Serrano', 'paula.serrano@example.com', 'pserrano', 'p@55w0rd30!', '1995-02-05', 'suspended'),
('Damián', 'Acosta', 'damian.acosta@example.com', 'dacosta', 'p@55w0rd31!', '1992-10-08', 'active'),
('Natalia', 'Padilla', 'natalia.padilla@example.com', 'npadilla', 'p@55w0rd32!', '1989-09-13', 'inactive'),
('Agustín', 'Rangel', 'agustin.rangel@example.com', 'arangel', 'p@55w0rd33!', '1987-12-24', 'active'),
('Josefina', 'Treviño', 'josefina.trevino@example.com', 'jtrevino', 'p@55w0rd34!', '1994-06-30', 'active'),
('Cristóbal', 'Delgado', 'cristobal.delgado@example.com', 'cdelgado', 'p@55w0rd35!', '1993-04-22', 'inactive'),
('Ximena', 'Carrillo', 'ximena.carrillo@example.com', 'xcarrillo', 'p@55w0rd36!', '1991-08-11', 'suspended'),
('Benjamín', 'Gallardo', 'benjamin.gallardo@example.com', 'bgallardo', 'p@55w0rd37!', '1988-07-20', 'active'),
('Antonella', 'Zamora', 'antonella.zamora@example.com', 'azamora', 'p@55w0rd38!', '1996-05-01', 'active'),
('Felipe', 'Moya', 'felipe.moya@example.com', 'fmoya', 'p@55w0rd39!', '1985-09-06', 'inactive'),
('Luciana', 'Salazar', 'luciana.salazar@example.com', 'lsalazar', 'p@55w0rd40!', '1992-02-28', 'active'),
('Gael', 'Reyes', 'gael.reyes@example.com', 'greyes', 'p@55w0rd41!', '1989-03-30', 'active'),
('Abril', 'Medina', 'abril.medina@example.com', 'amedina', 'p@55w0rd42!', '1995-10-04', 'suspended'),
('Bruno', 'Cano', 'bruno.cano@example.com', 'bcano', 'p@55w0rd43!', '1990-12-15', 'active'),
('María', 'Soto', 'maria.soto@example.com', 'msoto', 'p@55w0rd44!', '1987-06-12', 'active'),
('Thiago', 'Rivera', 'thiago.rivera@example.com', 'trivera', 'p@55w0rd45!', '1994-01-28', 'inactive'),
('Carla', 'Peralta', 'carla.peralta@example.com', 'cperalta', 'p@55w0rd46!', '1993-11-03', 'active'),
('Alan', 'Solís', 'alan.solis@example.com', 'asolis', 'p@55w0rd47!', '1986-07-19', 'suspended'),
('Elena', 'Vega', 'elena.vega@example.com', 'evega', 'p@55w0rd48!', '1991-03-06', 'active'),
('Franco', 'Ávila', 'franco.avila@example.com', 'favila', 'p@55w0rd49!', '1989-05-23', 'inactive'),
('Julia', 'Ponce', 'julia.ponce@example.com', 'jponce', 'p@55w0rd50!', '1990-10-18', 'active')
ON CONFLICT (email) DO NOTHING;


CREATE TABLE IF NOT EXISTS lyfter_car_rental.cars (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    brand VARCHAR(50) NOT NULL,
    model VARCHAR(50) NOT NULL,
    manufactured_year DATE NOT NULL,
    state VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- EXAMPLES

/*sql
brand VARCHAR(50) NOT NULL,
model VARCHAR(50) NOT NULL,
manufactured_year DATE NOT NULL,
state VARCHAR(50) NOT NULL
```

```

## Ejemplos de registros

| brand      | model   | manufactured_year | state     |
| ---------- | ------- | ------------------ | --------- |
| Toyota     | Corolla | 2018-05-01         | Excelente |
| Honda      | Civic   | 2016-03-15         | Muy bueno |
| Ford       | Focus   | 2014-07-20         | Bueno     |
| Nissan     | Sentra  | 2017-09-10         | Regular   |
| Kia        | Rio     | 2013-01-30         | Malo      |
| Chevrolet  | Aveo    | 2015-11-11         | Muy bueno |
| Hyundai    | Elantra | 2019-08-25         | Excelente |
| Volkswagen | Jetta   | 2012-06-18         | Bueno     |
| Mazda      | 3       | 2015-12-22         | Regular   |
| Suzuki     | Swift   | 2020-02-05         | Excelente |

```
*/


CREATE TABLE IF NOT EXISTS lyfter_car_rental.rentcar_users (
    id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id INT NOT NULL REFERENCES lyfter_car_rental.users(id) ON DELETE CASCADE,
    car_id INT NOT NULL REFERENCES lyfter_car_rental.cars(id) ON DELETE CASCADE,
    status VARCHAR(25) NOT NULL,
    rent_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
