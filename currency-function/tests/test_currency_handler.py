import sys
import types
from datetime import datetime

# --- Mock google.cloud.bigtable ---
class MockRow:
    def __init__(self, key):
        self.key = key
        self.cells = {}

    def set_cell(self, column_family, column, value):
        self.cells[(column_family, column)] = value

    def commit(self):
        print(f"Row committed: {self.key}")
        for k, v in self.cells.items():
            print(f"  {k}: {v}")

class MockTable:
    def direct_row(self, key):
        return MockRow(key)

class MockInstance:
    def table(self, table_id):
        return MockTable()

class MockClient:
    def __init__(self, project, admin):
        pass

    def instance(self, instance_id):
        return MockInstance()

# Replace the real bigtable client with our mock
sys.modules['google.cloud'] = types.ModuleType("google.cloud")
sys.modules['google.cloud.bigtable'] = types.ModuleType("google.cloud.bigtable")
import google.cloud.bigtable
google.cloud.bigtable.Client = MockClient

# --- Mock requests ---
import requests
class MockResponse:
    def json(self):
        return {'rates': {'INR': 83.25}}

requests.get = lambda url: MockResponse()

# --- Run the handler ---
from main import currency_handler

print("Running test_currency_handler()...")
currency_handler(event={}, context=None)
print("Test passed.")
