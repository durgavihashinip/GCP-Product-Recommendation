from google.cloud import bigtable

project_id = "pub-sub-1233"
instance_id = "currency-instance"
table_id = "currency-table"

client = bigtable.Client(project=project_id, admin=True)
instance = client.instance(instance_id)
table = instance.table(table_id)

rows = table.read_rows(limit=1)
for row in rows:
    print("Row key:", row.row_key.decode())
    for family_name, cells in row.cells.items():
        for column, cell_list in cells.items():
            print(f"{family_name}:{column.decode()} = {cell_list[0].value.decode()}")
