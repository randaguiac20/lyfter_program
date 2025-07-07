/* 
DROP TABLE owners;
DROP TABLE insurance_companies;
DROP TABLE car_colors;
DROP TABLE car_models;
DROP TABLE car_makers;
DROP TABLE maker_models;
DROP TABLE car_owners;
*/

SELECT * FROM owners;
SELECT * FROM insurance_companies;
SELECT * FROM car_models;
SELECT * FROM car_makers;
SELECT * FROM maker_models;
SELECT * FROM car_owners;
SELECT 
  o.name AS owner_name,
  cms.name AS maker,
  cm.name AS model,
  cl.name AS color,
  c.year,
  i.name AS insurance_company,
  i.policy AS insurance_policy
FROM car_owners c
JOIN owners o ON c.owner_id = o.id
JOIN car_colors cl ON c.color_id = cl.id
JOIN maker_models mm ON c.maker_model_id = mm.id
JOIN car_models cm ON mm.model_id = cm.id
JOIN car_makers cms ON mm.maker_id = cms.id
JOIN insurance_companies i ON c.insurance_id = i.id;
