# currency-function/tests/test_currency_handler.py

from google.cloud import bigtable

class MockClient:
    def __init__(self, *args, **kwargs):
        pass

    def table(self, table_id):
        return MockTable(table_id)  # Simulate returning a MockTable

class MockTable:
    def __init__(self, table_id):
        self.table_id = table_id

    def row(self, row_key):
        return MockRow(row_key)

class MockRow:
    def __init__(self, row_key):
        self.row_key = row_key

    def set_cell(self, *args, **kwargs):
        pass

def currency_handler(event, context):
    client = bigtable.Client(project="fake-project", admin=True)
    table = client.table("dummy_table_name")  # Use a real name if required here
    row = table.row("row-key")
    row.set_cell("cf1", "currency", "USD")

def test_currency_handler():
    event = {}
    context = {}
    currency_handler(event, context)
    print("Test passed!")

if __name__ == "__main__":
    test_currency_handler()
