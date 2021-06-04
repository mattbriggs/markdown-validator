import json
from azure.cosmosdb.table.tableservice import TableService
from azure.cosmosdb.table.models import Entity

with open(r"C:\git\mb\Azure-Stack-Doc-Projects-Python\Azure-Stack-Markdown-Auto\secrets.json") as fh:
    loaded_config = json.load(fh)

myaccount = loaded_config["myaccount"]
mykey = loaded_config["accountkey"]

table_service = TableService(account_name=myaccount, account_key=mykey)

table_service.create_table('testtable')

task = {'PartitionKey': 'tasksSeattle', 'RowKey': '001', 'description': 'Take out the trash', 'priority': 200}

table_service.insert_entity('testtable', task)