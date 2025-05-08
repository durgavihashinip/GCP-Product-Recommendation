# currency-function/tests/test_currency_handler.py

from google.cloud import bigtable

class MockClient:
    def __init__(self, *args, **kwargs):
        pass

    def table(self, table_id):
        return MockTable()

class MockTable:
    def row(self, row_key):
        return MockRow()

class MockRow:
    def set_cell(self, *args, **kwargs):
        pass

def currency_handler(event, context):
    client = bigtable.Client(project="fake-project", admin=True)
    table = client.table("dummy")
    row = table.row("row-key")
    row.set_cell("cf1", "currency", "USD")

def test_currency_handler():
    event = {}
    context = {}
    currency_handler(event, context)
    print("Test passed!")

if __name__ == "__main__":
    test_currency_handler()
