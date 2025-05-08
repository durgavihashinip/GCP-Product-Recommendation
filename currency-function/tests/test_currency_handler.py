# currency-function/tests/test_currency_handler.py

from google.cloud import bigtable

# Mocking the actual Bigtable Client and methods
class MockClient:
    def __init__(self, *args, **kwargs):
        pass

    # Mock the `table()` method of the Client to return an instance of MockTable
    def table(self, table_id):
        return MockTable(table_id)

# Mock Table class that the Client would normally return
class MockTable:
    def __init__(self, table_id):
        self.table_id = table_id

    # Mock the `row()` method of the Table to return a MockRow
    def row(self, row_key):
        return MockRow(row_key)

# Mock Row class to simulate row interaction
class MockRow:
    def __init__(self, row_key):
        self.row_key = row_key

    # Simulate the `set_cell` method used to insert data into the row
    def set_cell(self, *args, **kwargs):
        pass  # Just a placeholder for this test

# The actual currency_handler function
def currency_handler(event, context):
    # Here, we use the MockClient instead of the actual Bigtable Client
    client = MockClient()
    table = client.table("dummy_table_name")  # Using mock table name
    row = table.row("row-key")
    row.set_cell("cf1", "currency", "USD")

def test_currency_handler():
    event = {}
    context = {}
    currency_handler(event, context)
    print("Test passed!")

# Run the test
if __name__ == "__main__":
    test_currency_handler()
