import os
import datetime
from google.cloud import bigtable
from google.cloud import bigquery
from google.cloud.bigtable import row_set

def get_latest_rate_and_update_bq(event, context):
    project_id = "pub-sub-1233"
    bigquery_dataset_id = 'Staging_Layer'
    bigquery_rate_table_id = 'bq_latest_exchange_rate'
    bigtable_instance_id = 'currency-instance'
    bigtable_table_id = 'currency-table'

    client_bt = bigtable.Client(project=project_id, admin=True)
    instance = client_bt.instance(bigtable_instance_id)
    table = instance.table(bigtable_table_id)

    rs = row_set.RowSet()
    rs.add_row_range_from_keys(start_key=b"", end_key=b"~")  # Scan all rows

    rows = table.read_rows(row_set=rs)
    max_ts = datetime.datetime.min.replace(tzinfo=datetime.timezone.utc)
    found_rate = None

    for row in rows:
        try:
            row_key_str = row.row_key.decode('utf-8')
            current_ts = datetime.datetime.fromisoformat(row_key_str).replace(tzinfo=datetime.timezone.utc)

            if current_ts > max_ts:
                max_ts = current_ts
                if 'currency_data' in row.cells and b'inr' in row.cells['currency_data']:
                    found_rate = float(row.cells['currency_data'][b'inr'][0].value.decode('utf-8'))
        except Exception as e:
            print(f"Error processing row: {e}")
            continue

    if found_rate is None:
        print("No valid exchange rate found.")
        return

    client_bq = bigquery.Client(project=project_id)
    table_ref = client_bq.dataset(bigquery_dataset_id).table(bigquery_rate_table_id)

    merge_sql = f"""
    MERGE `{project_id}.{bigquery_dataset_id}.{bigquery_rate_table_id}` T
    USING (SELECT TIMESTAMP('{max_ts.isoformat()}') as ts, CAST({found_rate} AS FLOAT64) as rate) S
    ON FALSE
    WHEN NOT MATCHED THEN
      INSERT (rate_timestamp, inr_rate) VALUES(S.ts, S.rate)
    WHEN MATCHED THEN
      UPDATE SET T.rate_timestamp = S.ts, T.inr_rate = S.rate;
    """

    try:
        print(f"Running query: {merge_sql}")
        query_job = client_bq.query(merge_sql)
        query_job.result()
        print("BigQuery table updated successfully.")
    except Exception as e:
        print(f"Error updating BigQuery: {e}")
#check changes