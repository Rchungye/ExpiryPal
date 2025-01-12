CREATE DATABASE ExpiryPal;
USE ExpiryPal;


INSERT INTO camera(fridge_id, model, brand, accessURL, entity_id)
VALUES (1, "wi", "dlink", "variable", "camera.192_168_8_125");
select * from camera;


INSERT INTO fridge (id, model, brand, code) 
VALUES (1, 'Model X', 'Brand Y', 'FRIDGE123');
select * from fridge;


INSERT INTO item (fridge_id, name, addedDate, expirationDate, imageURL) VALUES
(1, 'Item 1', curdate(), DATE_ADD(CURDATE(), INTERVAL 1 DAY), 'https://i5.walmartimages.com/seo/Great-Value-Reduced-Fat-2-Milk-1-Gal_22a6459a-13b6-4057-aeae-45e62c69e8f8.47f793426ff66fa6432c948d836704f0.jpeg?odnHeight=2000&odnWidth=2000&odnBg=FFFFFF'),
(1, 'Item 2', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 2 DAY), 'https://i5.walmartimages.com/seo/Great-Value-White-Round-Top-Bread-20-oz_2e2a0e48-fecf-4b00-9ce4-64486788a22e.76317f2bfb5207c437cb7ccd4115589d.jpeg?odnHeight=2000&odnWidth=2000&odnBg=FFFFFF'),
(1, 'Item 3', '2024-12-13', DATE_ADD(CURDATE(), INTERVAL 3 DAY), 'https://i5.walmartimages.com/seo/Great-Value-Dr-Thunder-2-L_6fe14e57-a462-4387-8368-946b1cb6fb4f.18c630e8ad321fab0721fe23689eb53b.jpeg?odnHeight=2000&odnWidth=2000&odnBg=FFFFFF'),
(1, 'Item 4', '2024-12-14', DATE_ADD(CURDATE(), INTERVAL 4 DAY), 'https://i5.walmartimages.com/seo/FARMER-JOHN-HALF-HAM-BI_e4894832-8402-4c78-ba1b-5e510d08647a.8eb8e0b03c7eb97ccdf6fa1e017e9dee.jpeg?odnHeight=2000&odnWidth=2000&odnBg=FFFFFF'),
(1, 'Item 5', '2024-12-12', DATE_ADD(CURDATE(), INTERVAL 5 DAY), 'https://i5.walmartimages.com/seo/Butterball-Frozen-Whole-Turkey-All-Natural-10-16-lbs-Serves-5-8_9d0b65cc-f60b-4528-acce-8c0148c20d3e.4a9550a4c2e30e95e594591955c4859f.jpeg?odnHeight=2000&odnWidth=2000&odnBg=FFFFFF');
select * from item;


