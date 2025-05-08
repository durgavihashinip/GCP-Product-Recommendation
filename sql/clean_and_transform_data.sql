CREATE OR REPLACE PROCEDURE walmart_data.refresh_transformed_data()
BEGIN
  -- Step 1: Create cleaned_data
  CREATE OR REPLACE TABLE walmart_data.cleaned_data AS
  SELECT
    `Uniq Id`,
    `Product Id`,
    `Product Price`,
    IFNULL(`Product Rating`, 0) AS `Product_Rating`,
    IFNULL(`Product Reviews Count`, 0) AS `Product_Reviews_Count`,
    IFNULL(`Product Category`, '') AS `Product_Category`,
    IFNULL(`Product Brand`, '') AS `Product_Brand`,
    `Product Name`,
    `Product Image Url`,
    IFNULL(`Product Description`, '') AS `Product_Description`,
    `Product Tags`
  FROM
    walmart_data.data;

  -- Step 2: Create transformed_data
  CREATE OR REPLACE TABLE walmart_data.transformed_data AS
  WITH inr_rate_cte AS (
    SELECT inr_rate
    FROM (
      SELECT inr_rate, rate_timestamp
      FROM `pub-sub-1233.Staging_Layer.bq_latest_exchange_rate`
      ORDER BY rate_timestamp DESC
      LIMIT 1
    )
  )
  SELECT 
    c.*, 
    c.`Product Price` * r.inr_rate AS `Price_In_INR`
  FROM walmart_data.cleaned_data c
  CROSS JOIN inr_rate_cte r;
END;