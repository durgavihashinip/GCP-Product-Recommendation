-- Verify all transformed products exist in cleaned data
SELECT COUNT(*) AS orphaned_records
FROM walmart_data.transformed_data t
LEFT JOIN walmart_data.cleaned_data c
  ON t.`Product Id` = c.`Product Id`
WHERE c.`Product Id` IS NULL;