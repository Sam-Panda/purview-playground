from azure.purview.scanning import PurviewScanningClient
from azure.purview.catalog import PurviewCatalogClient
from azure.purview.administration.account import PurviewAccountClient
from azure.identity import ClientSecretCredential 
from azure.core.exceptions import HttpResponseError
import os
from dotenv import load_dotenv
from util.helper import Intialization 

i = Intialization()
subscription_id = i.subscription_id
purview_account_name = i.reference_name_purview

try:
  client = i.get_admin_client()
except ValueError as e:
    print(e)

collection_name = "AutomationTestColllection"
collection_list = client.collections.list_collections()
for collection in collection_list:
    # print(collection["friendlyName"])
    if collection["friendlyName"].lower() == collection_name.lower():
      collection_name = collection["name"]

# create scanning on sql server


scan_name = "test_scan_azure_sql_db"
datasource_name = "<<registereed-datasourcename-purview>>"
resource_endpoint = "<<sql-server-name>>.database.windows.net"
resource_id = f"/subscriptions/{subscription_id}/resourceGroups/<<resource_group_name>>/providers/Microsoft.Sql/servers/<<sql-server-name>>"
reference_name_purview = purview_account_name

databaseName = "<<database-name>>"


body_input = {
        "kind": "AzureSqlDatabaseMsi", # Authetication via the MSI
        "properties": {

            "collection": {
                "type": "CollectionReference",
                "referenceName": collection_name
            },
            "enableLineage": True,
            "recurrenceInterval":None,
            "serverEndpoint": resource_endpoint,
            "databaseName": databaseName,
            "scanRulesetName":"AzureSqlDatabase",
            "scanRulesetType":"System"            

        }
}

try:
    client = i.get_purview_client()
except ValueError as e:
    print(e)


try:
    response = client.scans.create_or_update(data_source_name=datasource_name, scan_name=scan_name, body=body_input)
    print(response)
except HttpResponseError as e:
    print(e)