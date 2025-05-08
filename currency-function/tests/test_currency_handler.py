import unittest
from unittest.mock import patch, MagicMock
from main import currency_handler

class TestCurrencyHandler(unittest.TestCase):

    @patch('main.requests.get')
    @patch('main.bigtable.Client')
    def test_currency_handler_success(self, mock_bigtable_client, mock_requests_get):
        # Mock API response
        mock_requests_get.return_value.json.return_value = {
            'rates': {'INR': 83.21}
        }

        # Mock Bigtable client and related calls
        mock_instance = MagicMock()
        mock_table = MagicMock()
        mock_row = MagicMock()

        mock_bigtable_client.return_value.instance.return_value = mock_instance
        mock_instance.table.return_value = mock_table
        mock_table.direct_row.return_value = mock_row

        # Call the function
        currency_handler(None, None)

        # Assertions
        mock_requests_get.assert_called_once_with("https://api.exchangerate-api.com/v4/latest/USD")
        mock_bigtable_client.assert_called_once()
        mock_instance.table.assert_called_once_with("currency-table")
        mock_table.direct_row.assert_called()
        mock_row.set_cell.assert_any_call("currency_data", "usd", "1")
        mock_row.set_cell.assert_any_call("currency_data", "inr", "83.21")
        mock_row.set_cell.assert_any_call("currency_data", "timestamp", unittest.mock.ANY)
        mock_row.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
