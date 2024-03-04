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
    print(collection["friendlyName"])
    if collection["friendlyName"].lower() == collection_name.lower():
      collection_name = collection["name"]


## registering the data source ( blob storage) 

ds_name = "ds4mapi_blob_functionstorage32zn"

storage_name = "<<storage-account-name>>"
storage_id = f"/subscriptions/{subscription_id}/resourceGroups/<<resource-group-name>>/providers/Microsoft.Storage/storageAccounts/<<storage-account-name>>"
rg_name = "<<resource-group-name>>"
rg_location = "<<resource-group-location>>"
reference_name_purview = purview_account_name



body_input = {
        "kind": "AzureStorage",
        "properties": {
            "endpoint": f"https://{storage_name}.blob.core.windows.net/",
            "resourceGroup": rg_name,
            "location": rg_location,
            "resourceName": storage_name,
            "resourceId": storage_id,
            "collection": {
                "type": "CollectionReference",
                "referenceName": collection_name
            },
            "dataUseGovernance": "Disabled"
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