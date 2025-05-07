# rate_updater/test_main.py
import unittest
from unittest.mock import patch, MagicMock
from main import get_latest_rate_and_update_bq
from datetime import datetime, timezone

class TestRateUpdaterFunction(unittest.TestCase):

    @patch('google.cloud.bigtable.Client')
    @patch('google.cloud.bigquery.Client')
    def test_get_latest_rate_and_update_bq_success(self, mock_bigquery_client, mock_bigtable_client):
        # Mock Bigtable data
        mock_instance = mock_bigtable_client.return_value.instance.return_value
        mock_table = mock_instance.table.return_value
        mock_row1 = MagicMock(row_key=b"2025-05-07T00:00:00.000000+00:00", cells={'currency_data': {b'inr': [MagicMock(value=b'81.0')]}})
        mock_row2 = MagicMock(row_key=b"2025-05-06T23:59:00.000000+00:00", cells={'currency_data': {b'inr': [MagicMock(value=b'80.5')]}})
        mock_table.read_rows.return_value = [mock_row1, mock_row2]

        # Mock BigQuery client and query job
        mock_bq_client = mock_bigquery_client.return_value
        mock_query_job = mock_bq_client.query.return_value
        mock_query_job.result.return_value = None

        get_latest_rate_and_update_bq(None, None)

        # Assert Bigtable interaction
        mock_table.read_rows.assert_called_once()

        # Assert BigQuery interaction
        mock_bq_client.query.assert_called_once()
        sql_query = mock_bq_client.query.call_args[0][0]
        self.assertIn("MERGE `pub-sub-1233.Staging_Layer.bq_latest_exchange_rate`", sql_query)
        self.assertIn("CAST(81.0 AS FLOAT64) as rate", sql_query)

    def test_get_latest_rate_and_update_bq_no_rate_found(self):
        mock_bigtable_client = MagicMock()
        mock_instance = mock_bigtable_client.return_value.instance.return_value
        mock_table = mock_instance.table.return_value
        mock_table.read_rows.return_value = []  # No rows

        mock_bigquery_client = MagicMock()

        get_latest_rate_and_update_bq(None, None)

        mock_bigquery_client.query.assert_not_called() # Ensure BigQuery wasn't updated

if __name__ == '__main__':
    unittest.main()
