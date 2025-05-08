-- Check NULLs removed from Product Rating
SELECT COUNT(*) AS null_ratings
FROM walmart_data.cleaned_data
WHERE `Product_Price` IS NULL;

