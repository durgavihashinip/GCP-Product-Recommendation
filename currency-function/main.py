import requests
from google.cloud import bigtable
from datetime import datetime

def currency_handler(event, context):
    # Call the external API
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    data = response.json()
    inr_rate = data['rates']['INR']
    timestamp = datetime.utcnow().isoformat()

    # Hardcoded Bigtable config
    project_id = "pub-sub-1233"
    instance_id = "currency-instance"
    table_id = "currency-table"

    # Connect to Bigtable
    client = bigtable.Client(project=project_id, admin=True)
    instance = client.instance(instance_id)
    table = instance.table(table_id)

    # Create row with timestamp as key
    row = table.direct_row(timestamp.encode())
    row.set_cell("currency_data", "usd", "1")
    row.set_cell("currency_data", "inr", str(inr_rate))
    row.set_cell("currency_data", "timestamp", timestamp)
    row.commit()
