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


## registering the data source ( blob storage)

ds_name = "ds4mapi_azuresqlserver_opnhckdasqlsvr"

resource_name = "opnhckdasqlsvr"
resource_endpoint = "opnhckdasqlsvr.database.windows.net"
resource_id = f"/subscriptions/{subscription_id}/resourceGroups/openhack_data_analytics/providers/Microsoft.Sql/servers/opnhckdasqlsvr"
rg_name = "openhack_data_analytics"
rg_location = "eastus"
reference_name_purview = purview_account_name



body_input = {
        "kind": "AzureSqlDatabase",
        "properties": {
            "serverEndpoint": resource_endpoint,
            "resourceGroup": rg_name,
            "location": rg_location,
            "resourceName": resource_name,
            "resourceId": resource_id,
            "collection": {
                "type": "CollectionReference",
                "referenceName": collection_name
            },
            "dataUseGovernance": "Enabled",
            "subscriptionId": subscription_id
        }
}

try:
    client = i.get_purview_client()
except ValueError as e:
    print(e)

try:
    response = client.data_sources.create_or_update(ds_name, body=body_input)
    print(response)
    print(f"Data source {ds_name} successfully created or updated")
except HttpResponseError as e:
    print(e)