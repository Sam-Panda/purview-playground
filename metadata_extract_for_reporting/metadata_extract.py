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
collection_name = "Marketing"


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

# Filter the objects that has classification assigned

objects_with_classification = [obj for obj in response['value'] if 'classification' in obj.keys()]

# traverse through the objects which has the classification keys
outputs = []
for obj in objects_with_classification:
    endpoint=f"https://{reference_name_purview}.purview.azure.com"
    guid = obj["id"]

    catalog_client = get_catalog_client(reference_name_purview)
    #getting the details of the entity, for example Table.
    entity_response = catalog_client.entity.get_by_guid(guid)
    # getting the details of the columns by extracting out the referredEntities from the response.
    response_referredEntities = entity_response['referredEntities']
    columns_guids = response_referredEntities.keys()


    for column_guid in columns_guids:
        column_metadata = response_referredEntities[column_guid]
        # check if the column has classification
        if 'classifications' in column_metadata.keys():
            qualifiedName = column_metadata['attributes']['qualifiedName']
            table_name = qualifiedName.split("/")[-1].split("#")[0]
            column_name = qualifiedName.split("/")[-1].split("#")[-1]
            print(f"Table Name: {table_name}")  
            print(f"Column Name: {column_name}")      
            classifications = column_metadata['classifications']
            for classification in classifications:
                print(f"Classification: {classification['typeName']}")
                outputs.append({"TableName": table_name, "ColumnName": column_name, "qualifiedName": qualifiedName, "Classification": classification['typeName']})
            

df = pd.DataFrame(outputs)
df.to_csv("classification_report.csv", index=False)
print("Classification report is generated and saved as classification_report.csv")






