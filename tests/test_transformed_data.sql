-- Verify INR conversion exists
SELECT COUNT(*) AS missing_inr_prices
FROM walmart_data.transformed_data
WHERE Price_In_INR IS NULL;

-- Verify exchange rate is reasonable
SELECT 
  MIN(Price_In_INR/`Product Price`) AS min_rate,
  MAX(Price_In_INR/`Product Price`) AS max_rate
FROM walmart_data.transformed_data
WHERE `Product Price` > 0;