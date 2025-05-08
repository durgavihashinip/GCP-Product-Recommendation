import sys
import types
import datetime

# --- Mock Bigtable ---
class MockCell:
    def __init__(self, value):
        self.value = value.encode('utf-8')

class MockRow:
    def __init__(self, row_key, rate):
        self.row_key = row_key.encode('utf-8')
        self.cells = {
            'currency_data': {
                b'inr': [MockCell(str(rate))]
            }
        }

class MockRowSet:
    def add_row_range_from_keys(self, start_key, end_key):
        pass

class MockTable:
    def read_rows(self, row_set=None):
        now = datetime.datetime.utcnow().isoformat()
        return [MockRow(now, 83.55)]

class MockInstance:
    def table(self, table_id):
        return MockTable()

class MockBigtableClient:
    def __init__(self, project, admin):
        pass
    def instance(self, instance_id):
        return MockInstance()

# --- Mock BigQuery ---
class MockQueryJob:
    def result(self):
        print("Simulated BigQuery execution.")

class MockBigQueryClient:
    def __init__(self, project):
        pass
    def dataset(self, dataset_id):
        class DatasetRef:
            def table(self, table_id):
                return f"{dataset_id}.{table_id}"
        return DatasetRef()
    def query(self, sql):
        print("Simulated SQL:\n", sql)
        return MockQueryJob()

# --- Inject mocks into sys.modules ---
sys.modules['google.cloud'] = types.ModuleType("google.cloud")
sys.modules['google.cloud.bigtable'] = types.ModuleType("google.cloud.bigtable")
sys.modules['google.cloud.bigtable.row_set'] = types.ModuleType("google.cloud.bigtable.row_set")
sys.modules['google.cloud.bigquery'] = types.ModuleType("google.cloud.bigquery")

import google.cloud.bigtable
import google.cloud.bigtable.row_set
import google.cloud.bigquery

google.cloud.bigtable.Client = MockBigtableClient
google.cloud.bigtable.row_set = types.SimpleNamespace(RowSet=MockRowSet)
google.cloud.bigquery.Client = MockBigQueryClient

# --- Run the function ---
from main import get_latest_rate_and_update_bq

print("Running test_get_latest_rate_and_update_bq()...")
get_latest_rate_and_update_bq(event={}, context=None)
print("Test passed.")
