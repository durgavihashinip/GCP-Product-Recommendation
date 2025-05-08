-- Verify new records are arriving
SELECT
  COUNT(*) AS record_count,
  MIN(rate_timestamp) AS oldest_record,
  MAX(rate_timestamp) AS newest_record
FROM `pub-sub-1233.Staging_Layer.bq_latest_exchange_rate`
WHERE rate_timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY)