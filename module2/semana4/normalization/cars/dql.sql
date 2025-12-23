
SELECT * FROM owners;
SELECT * FROM insurance_companies;
SELECT * FROM car_colors;
SELECT * FROM car_models;
SELECT * FROM car_makers;
SELECT * FROM cars;
SELECT 
  o.name AS owner_name,
  cms.name AS maker,
  cm.name AS model,
  cc.name AS color,
  c.year,
  i.name AS insurance_company,
  i.policy AS insurance_policy
FROM cars c
JOIN owners o ON c.owner_id = o.id
JOIN car_makers cms ON c.maker_id = cms.id
JOIN car_models cm ON c.maker_id = cm.id
JOIN car_colors cc ON c.color_id = cc.id
JOIN insurance_companies i ON c.insurance_id = i.id;
