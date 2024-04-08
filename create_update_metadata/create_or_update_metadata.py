from azure.purview.scanning import PurviewScanningClient
from azure.purview.catalog import PurviewCatalogClient
from azure.purview.administration.account import PurviewAccountClient
from azure.identity import ClientSecretCredential 
from azure.core.exceptions import HttpResponseError
import os, json, requests
from dotenv import load_dotenv
import pandas as pd
from azure.identity import AzureCliCredential
import pandas as pd

# give the child collection name where we have the assets
collection_name = "ScopedScanningAutomation"


load_dotenv()
# reading the variables from .env file  
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
reference_name_purview = os.getenv("PURVIEW_ACCOUNT_NAME")



def get_credentials():
    # credentials = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    credentials = AzureCliCredential()
    return credentials


def get_catalog_client(reference_name_purview):
    credentials = get_credentials()
    client = PurviewCatalogClient(endpoint=f"https://{reference_name_purview}.purview.azure.com/", credential=credentials, logging_enable=True)
    return client

def get_admin_client(reference_name_purview):
    credentials = get_credentials()
    client = PurviewAccountClient(endpoint=f"https://{reference_name_purview}.purview.azure.com/", credential=credentials, logging_enable=True)
    return client

def get_collection_Id(collection_name):
    try:
        client = get_admin_client(reference_name_purview)
    except ValueError as e:
        print(e)
    collection_name_unique_id = ''
    #collection_name = "AutomationTestColllection"
    collection_list = client.collections.list_collections()
    for collection in collection_list:
        # print(collection["friendlyName"])
        if collection["friendlyName"].lower() == collection_name.lower():
            collection_name_unique_id = collection["name"]
    return collection_name_unique_id


def queryCollection( collection_name, reference_name_purview):

    purview_endpoint = f"https://{reference_name_purview}.purview.azure.com"
    payload= {
        "keywords": "*",
        "filter": {
            "and" : [
                {
                    "or" :[
                        {
                            "collectionId":get_collection_Id(collection_name)
                        }
                    ]
                }
            ]
        }
        }
    
    # create the catalog client
    try:
        catalog_client = get_catalog_client(reference_name_purview)
    except ValueError as e:
        print(e)

    json_results = catalog_client.discovery.query(payload)
    
    return json_results


# execution 

# getting all the metadata from the collection
response = queryCollection( collection_name, reference_name_purview)
assets= response['value']

# read the assets information from the csv file that needs to be updated

# read the csv file
df = pd.read_csv("assetinfo.csv")

# filter the assets that we have in the csv file            

assets_to_update = [asset for asset in assets if asset['name'] in df['AssetName'].tolist()]

# update the metadata of the assets

for asset in assets_to_update:
    catalog_client = get_catalog_client(reference_name_purview)
    asset_name = asset['name']
    asset_id = asset['id']
    print(f"Updating metadata for asset: {asset_name}")
    #getting the details of the entity, for example Table.
    entity_response = catalog_client.entity.get_by_guid(asset_id)
    _entity_response = entity_response
    # # remove the userDescription field from _entity_response['entity']['attributes']['userDescription']
    _entity_response['entity']['attributes'].pop('userDescription', None)
    # add the userDescription field from the csv file
    _entity_response['entity']['attributes']['userDescription'] = df[df['AssetName']==asset_name]['AssetDescription'].values[0]
    catalog_client.entity.create_or_update(_entity_response)







