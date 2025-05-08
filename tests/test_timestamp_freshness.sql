-- Check if latest record is recent
SELECT 
  TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), MAX(rate_timestamp), MINUTE) AS minutes_since_last_update
FROM `pub-sub-1233.Staging_Layer.bq_latest_exchange_rate`