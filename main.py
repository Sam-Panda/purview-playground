from azure.purview.scanning import PurviewScanningClient
from azure.purview.catalog import PurviewCatalogClient
from azure.purview.administration.account import PurviewAccountClient
from azure.identity import ClientSecretCredential 
from azure.core.exceptions import HttpResponseError
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")

reference_name_purview = os.getenv("PURVIEW_ACCOUNT_NAME")


def get_credentials():
    credentials = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    return credentials

def get_purview_client():
    credentials = get_credentials()
    client = PurviewScanningClient(endpoint=f"https://{reference_name_purview}.scan.purview.azure.com", credential=credentials, logging_enable=True)  
    return client

def get_catalog_client():
    credentials = get_credentials()
    client = PurviewCatalogClient(endpoint=f"https://{reference_name_purview}.purview.azure.com/", credential=credentials, logging_enable=True)
    return client

def get_admin_client():
    credentials = get_credentials()
    client = PurviewAccountClient(endpoint=f"https://{reference_name_purview}.purview.azure.com/", credential=credentials, logging_enable=True)
    return client

try:
  client = get_admin_client()
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

storage_name = "functionstorage32zn"
storage_id = "/subscriptions/89c37dd8-94bb-4870-98e0-1cfb98c0262e/resourceGroups/ADBPVlineagev3/providers/Microsoft.Storage/storageAccounts/functionstorage32zn"
rg_name = "ADBPVlineagev3"
rg_location = "Central US"
reference_name_purview = reference_name_purview



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
    client = get_purview_client()
except ValueError as e:
    print(e)

try:
    response = client.data_sources.create_or_update(ds_name, body=body_input)
    print(response)
    print(f"Data source {ds_name} successfully created or updated")
except HttpResponseError as e:
    print(e)