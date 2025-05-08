-- Check for missing critical values
SELECT 
  COUNT(*) AS total_rows,
  COUNTIF(`Product Id` IS NULL) AS missing_ids,
  COUNTIF(`Product Name` IS NULL) AS missing_names,
  COUNTIF(`Product Price` IS NULL) AS missing_prices
FROM walmart_data.transformed_data;
