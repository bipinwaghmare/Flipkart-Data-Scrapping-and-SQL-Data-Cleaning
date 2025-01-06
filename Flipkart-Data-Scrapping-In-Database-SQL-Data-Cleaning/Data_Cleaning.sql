create database flipkart_database;

use flipkart_database;

select * from flipkart_mobiles;
##
UPDATE flipkart_mobiles
SET Price = REPLACE(REPLACE(Price, '₹', ''), ',', '');
##
UPDATE flipkart_mobiles
SET Product_name = REGEXP_REPLACE(Product_name, '\\s*\\(.*?\\)', '');
##
ALTER TABLE flipkart_mobiles ADD is_5G VARCHAR(3);

UPDATE flipkart_mobiles
SET is_5G = CASE
    WHEN Product_name LIKE '%5G%' THEN 'Yes'
    ELSE 'No'
END;
##
-- Add columns for RAM and ROM
ALTER TABLE flipkart_mobiles ADD RAM_in_GB VARCHAR(50);
ALTER TABLE flipkart_mobiles ADD ROM_in_GB VARCHAR(50);

-- Extract RAM
UPDATE flipkart_mobiles
SET RAM_in_GB = REGEXP_SUBSTR(Storage, '\\d+\\s?GB RAM');

-- Extract ROM
UPDATE flipkart_mobiles
SET ROM_in_GB = REGEXP_SUBSTR(Storage, '\\d+\\s?GB ROM');

-- Remove the `Storage` column if no longer needed
ALTER TABLE flipkart_mobiles DROP COLUMN Storage;
##
-- Add columns for display type and size
ALTER TABLE flipkart_mobiles ADD Display_type VARCHAR(255);
ALTER TABLE flipkart_mobiles ADD Display_size_in_inch VARCHAR(50);

-- Extract display type (text after the parentheses)
UPDATE flipkart_mobiles
SET Display_type = TRIM(SUBSTRING_INDEX(Display_size, ') ', -1));

-- Extract display size (text inside the parentheses)
UPDATE flipkart_mobiles
SET Display_size_in_inch = TRIM(SUBSTRING(
    Display_size,
    LOCATE('(', Display_size) + 1,
    LOCATE(')', Display_size) - LOCATE('(', Display_size) - 1
));

-- Remove the `Display_size` column if no longer needed
ALTER TABLE flipkart_mobiles DROP COLUMN Display_size;
##

-- Add columns for rear and front cameras
ALTER TABLE flipkart_mobiles ADD Rear_camera_in_MP INT;
ALTER TABLE flipkart_mobiles ADD Front_camera_in_MP INT;

-- Extract highest MP for rear camera
UPDATE flipkart_mobiles
SET Rear_camera_in_MP = (
    SELECT MAX(CAST(REPLACE(TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(Camera_Details, '+', numbers.n), '+', -1)), 'MP', '') AS UNSIGNED))
    FROM (
        SELECT 1 AS n UNION SELECT 2 UNION SELECT 3 UNION SELECT 4 UNION SELECT 5
    ) numbers
    WHERE Camera_Details LIKE '%|%'
      AND SUBSTRING_INDEX(Camera_Details, '|', 1) LIKE CONCAT('%', SUBSTRING_INDEX(Camera_Details, '+', numbers.n), '%')
);

-- Extract highest MP for front camera
UPDATE flipkart_mobiles
SET Front_camera_in_MP = CAST(
    REPLACE(
        TRIM(SUBSTRING_INDEX(Camera_Details, '|', -1)),
        'MP Front Camera', ''
    ) AS UNSIGNED
)
WHERE Camera_Details LIKE '%|%';
##

ALTER TABLE flipkart_mobiles ADD Battery_capacity_in_mAh INT;

UPDATE flipkart_mobiles
SET Battery_capacity_in_mAh = CAST(REGEXP_SUBSTR(Battery, '\\d+') AS INT);

-- Drop the `Battery` column if no longer needed
ALTER TABLE flipkart_mobiles DROP COLUMN Battery;
##

UPDATE flipkart_mobiles
SET Warranty = CASE
    WHEN Warranty LIKE '%1%' OR Warranty LIKE '%12%' THEN 1
    WHEN Warranty LIKE '%2%' OR Warranty LIKE '%24%' THEN 2
    ELSE NULL
END;
##

ALTER TABLE flipkart_mobiles ADD Processor_brand VARCHAR(50);

UPDATE flipkart_mobiles
SET Processor_brand = CASE
    WHEN Processor LIKE '%Qualcomm%' OR Processor LIKE '%Snapdragon%' THEN 'Snapdragon'
    WHEN Processor LIKE '%Helio%' THEN 'Mediatek Helio'
    WHEN Processor LIKE '%Dimensity%' THEN 'Mediatek Dimensity'
    WHEN Processor LIKE '%Unisoc%' THEN 'Unisoc'
    ELSE 'Other'
END;

-- Drop the `Processor` column if no longer needed
ALTER TABLE flipkart_mobiles DROP COLUMN Processor;
##

-- Add columns for ratings and reviews
ALTER TABLE flipkart_mobiles ADD Total_Ratings INT;
ALTER TABLE flipkart_mobiles ADD Total_Reviews INT;

-- Extract ratings
UPDATE flipkart_mobiles
SET Total_Ratings = CAST(REGEXP_SUBSTR(Overall_Review, '\\d+ Ratings') AS INT);

-- Extract reviews
UPDATE flipkart_mobiles
SET Total_Reviews = CAST(REGEXP_SUBSTR(Overall_Review, '\\d+ Reviews') AS INT);

-- Drop the `Overall_Review` column if no longer needed
ALTER TABLE flipkart_mobiles DROP COLUMN Overall_Review;
##

ALTER TABLE flipkart_mobiles ADD product_brand VARCHAR(255);

UPDATE flipkart_mobiles
SET product_brand = SUBSTRING_INDEX(Product_name, ' ', 1);
##

UPDATE flipkart_mobiles
SET Price = NULL
WHERE Price = 'Not Available';

DELETE FROM flipkart_mobiles
WHERE Price IS NULL;
##

ALTER TABLE flipkart_mobiles MODIFY Price DECIMAL(10, 2);
ALTER TABLE flipkart_mobiles MODIFY Total_Ratings INT;
ALTER TABLE flipkart_mobiles MODIFY Total_Reviews INT;
ALTER TABLE flipkart_mobiles MODIFY Battery_capacity_in_mAh INT;
ALTER TABLE flipkart_mobiles MODIFY RAM_in_GB FLOAT;
ALTER TABLE flipkart_mobiles MODIFY ROM_in_GB FLOAT;
ALTER TABLE flipkart_mobiles MODIFY Display_size_in_inch FLOAT;
##

ALTER TABLE flipkart_mobiles DROP COLUMN Camera_Details;




select * from flipkart_mobiles;