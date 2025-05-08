# Mock Client class to simulate a BigQuery client
class MockClient:
    def dataset(self, dataset_id):
        return MockDataset(dataset_id)

    def query(self, sql):
        print(f"Executing SQL: {sql}")
        return MockQueryJob()

# Mock Dataset class
class MockDataset:
    def __init__(self, dataset_id):
        self.dataset_id = dataset_id

    def table(self, table_id):
        return f"{self.dataset_id}.{table_id}"

# Mock QueryJob class
class MockQueryJob:
    def result(self):
        print("Simulated BigQuery query execution.")

# The get_latest_rate_and_update_bq function using mocked classes
def get_latest_rate_and_update_bq(event, context):
    client = MockClient()
    dataset = client.dataset("mock_dataset")
    table = dataset.table("mock_table")

    sql = f"INSERT INTO `{table}` (currency, rate) VALUES ('INR', 83.55);"
    query_job = client.query(sql)
    query_job.result()

# Simple test function
def test_get_latest_rate_and_update_bq():
    event = {}
    context = {}
    get_latest_rate_and_update_bq(event, context)
    print("Test passed!")

# Run test
if __name__ == "__main__":
    test_get_latest_rate_and_update_bq()
