from azure.purview.scanning import PurviewScanningClient
from azure.purview.catalog import PurviewCatalogClient
from azure.purview.administration.account import PurviewAccountClient
from azure.identity import ClientSecretCredential 
from azure.core.exceptions import HttpResponseError
import os
from dotenv import load_dotenv
from util.helper import Intialization 
import pandas as pd

i = Intialization()
subscription_id = i.subscription_id
purview_account_name = i.reference_name_purview

try:
  client = i.get_admin_client()
except ValueError as e:
    print(e)




# Delete all the assests for the collection given below.
###############################################

# declare the collection name

collection_name = "AutomationTestColllection"

collection_list = client.collections.list_collections()
for collection in collection_list:
    # print(collection["friendlyName"])
    if collection["friendlyName"].lower() == collection_name.lower():
      collection_name = collection["name"]

# create the catalog client
try:
    catalog_client = i.get_catalog_client()
except ValueError as e:
    print(e)

payload= {
    "limit": 100,
    "keywords": "*",
    "filter": {
        "and" : [
            {
                "or" :[
                    {
                        "collectionId":collection_name
                    }
                ]
            }
        ]
    }
    }

json_results = catalog_client.discovery.query(payload)
guids = []
df = pd.DataFrame(columns=['guid', 'qualifiedName'])

for entity in json_results["value"]:
    guid = entity["id"]
    qualifiedName = entity["qualifiedName"]
    df = df.append({'guid' : guid, 'qualifiedName': qualifiedName}, ignore_index=True)
    print(f"GUID: {guid} qualifiedName: {qualifiedName}")
    guids.append(entity["id"])

# save the content that we are going to delete in a csv
file_path = os.path.join(os.getcwd(),"OutputFiles", "outputAssests.csv")
df.to_csv(file_path, index=False)

# We are going to deleteall the Guids. I have commented out this to avoid any accidental delete.
# catalog_client.entity.delete_by_guids(guids=guids)
