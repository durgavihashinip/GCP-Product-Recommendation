# currency-function/test_main.py
import unittest
from unittest.mock import patch
from main import currency_handler

class TestCurrencyFunction(unittest.TestCase):

    @patch('requests.get')
    @patch('google.cloud.bigtable.Client')
    def test_currency_handler_success(self, mock_bigtable_client, mock_get):
        # Mock the API response
        mock_response = mock_get.return_value
        mock_response.json.return_value = {'rates': {'INR': 80.0}}

        # Mock Bigtable objects (simplified)
        mock_instance = mock_bigtable_client.return_value.instance.return_value
        mock_table = mock_instance.table.return_value
        mock_row = mock_table.direct_row.return_value

        currency_handler(None, None)

        # Assert that the API was called
        mock_get.assert_called_once_with("https://api.exchangerate-api.com/v4/latest/USD")
        # Assert that Bigtable was interacted with (basic check)
        mock_bigtable_client.assert_called_once()
        mock_instance.table.assert_called_once_with("currency-table")
        mock_table.direct_row.assert_called()
        mock_row.set_cell.assert_any_call("currency_data", "inr", "80.0")

if __name__ == '__main__':
    unittest.main()