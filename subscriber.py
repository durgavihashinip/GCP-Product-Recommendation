import json
import requests
import logging
from datetime import datetime
from google.cloud import bigtable

# def callback(event, context):
#     try:
#         url = "https://api.exchangeratesapi.io/v1/latest?access_key=995533cf338c682cac2d6c2277f2ba0c&format=1"
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()

#         data = response.json()
#         if not data.get("success", False):
#             raise ValueError("API response unsuccessful")

#         date = data['date']
#         inr = data['rates'].get('INR')
#         usd = data['rates'].get('USD', 1)  # fallback

#         client = bigtable.Client(project='sodium-chalice-458311-g3', admin=True)
#         instance = client.instance('exchange-instance')
#         table = instance.table('conversion_rates')

#         row_key = date.encode('utf-8')
#         bt_row = table.direct_row(row_key)
#         bt_row.set_cell('rates', 'USD', str(usd))
#         bt_row.set_cell('rates', 'INR', str(inr))
#         bt_row.set_cell('meta', 'timestamp', datetime.utcnow().isoformat())
#         bt_row.commit()

#         logging.info(f"Success: Stored rates for {date}")

#     except Exception as e:
#         logging.error(f"Error fetching or storing data: {str(e)}")
#         raise

def callback(event, context):
    import logging
    logging.info("Callback triggered with event: %s", event)

    try:
        response = requests.get("https://api.exchangeratesapi.io/v1/latest?access_key=995533cf338c682cac2d6c2277f2ba0c&format=1")
        data = response.json()
        logging.info(f"Fetched data: {data}")

        date = data['date']
        inr = data['rates'].get('INR')
        usd = data['rates'].get('USD', 1)

        client = bigtable.Client(project='sodium-chalice-458311-g3', admin=True)
        instance = client.instance('exchange-instance')
        table = instance.table('conversion_rates')

        row_key = date.encode('utf-8')
        bt_row = table.direct_row(row_key)
        bt_row.set_cell('rates', 'USD', str(usd))
        bt_row.set_cell('rates', 'INR', str(inr))
        bt_row.set_cell('meta', 'timestamp', datetime.utcnow().isoformat())
        bt_row.commit()

        logging.info(f"Written to Bigtable: {date}, USD={usd}, INR={inr}")
    except Exception as e:
        logging.error("Error in subscriber callback: %s", str(e))
