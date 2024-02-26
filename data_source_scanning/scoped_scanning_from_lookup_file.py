from azure.purview.scanning import PurviewScanningClient
from azure.purview.catalog import PurviewCatalogClient
from azure.purview.administration.account import PurviewAccountClient
from azure.identity import ClientSecretCredential 
from azure.core.exceptions import HttpResponseError
import os
from dotenv import load_dotenv
import pandas as pd
from azure.identity import AzureCliCredential

load_dotenv()
# reading the variables from .env file  
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
tenant_id = os.getenv("TENANT_ID")
reference_name_purview = os.getenv("PURVIEW_ACCOUNT_NAME")
subscription_id = os.getenv("SUBSCRIPTION_ID")
resource_endpoint = os.getenv("RESOURCE_ENDPOINT")
databasename = os.getenv("DATABASE_NAME")
#declare variables 

purview_registered_datasource_name = os.getenv("PURVIEW_REGISTERED_DATASOURCE_NAME")


def get_credentials():
    # credentials = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id)
    credentials = AzureCliCredential()
    return credentials

def get_admin_client(reference_name_purview):
    credentials = get_credentials()
    client = PurviewAccountClient(endpoint=f"https://{reference_name_purview}.purview.azure.com/", credential=credentials, logging_enable=True)
    return client

def get_purview_client(reference_name_purview):
    credentials = get_credentials()
    client = PurviewScanningClient(endpoint=f"https://{reference_name_purview}.scan.purview.azure.com", credential=credentials, logging_enable=True)  
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


# create scanning on sql server

# scan_name = "test_scan_azure_sql_db_v3"
def create_default_scan (scan_name, collection_name_unique_id):

    body_input = {
            "kind": "AzureSqlDatabaseCredential",
            "properties": {

                "collection": {
                    "type": "CollectionReference",
                    "referenceName": collection_name_unique_id
                },
                "credential": {
                        "referenceName": "sapa-WideWorldImporters-cred",
                        "credentialType": "SqlAuth"
                },

                "enableLineage": False,
                "recurrenceInterval":None,
                "serverEndpoint": resource_endpoint,
                "databaseName": databasename,
                "scanRulesetName":"AzureSqlDatabase",
                "scanRulesetType":"System"
            }
    }
    print (body_input)
    try:
        client = get_purview_client(reference_name_purview)
    except ValueError as e:
        print(e)


    try:
        response = client.scans.create_or_update(data_source_name=purview_registered_datasource_name, scan_name=scan_name, body=body_input)
        print(response)
    except HttpResponseError as e:
        print(e)

def apply_filter_on_scan(scan_name, lstexcludeUriPrefixes, lstincludeUriPrefixes):
    
    try:
        client = get_purview_client(reference_name_purview)
    except ValueError as e:
        print(e)

    filter_body_input = {
    "properties":{
        "excludeUriPrefixes":lstexcludeUriPrefixes,
        "includeUriPrefixes":lstincludeUriPrefixes,
        "excludeRegexes":None,
        "includeRegexes":None
        }
     }
    print (filter_body_input)
    client.filters.create_or_update(data_source_name=purview_registered_datasource_name, scan_name=scan_name, body=filter_body_input)




# read the csv files
file_path = os.path.join(os.getcwd(),"InputFiles", "assestsToBeScanned.csv")
df_csv = pd.read_csv(file_path)
unique_scan_names = df_csv["scanName"].unique()
for scan_name in unique_scan_names:
    if scan_name != "exclude":  
        lst_unique_qualified_names = df_csv["assetqualifiedDomain"].unique().tolist()
        df_csv_filtered = df_csv.query(f"scanName == '{scan_name}'")
        collection_name = df_csv_filtered["collectionName"].unique()[0]
        collection_name_unique_id = get_collection_Id(collection_name)
        lst_included_qualified_names = df_csv_filtered["assetqualifiedDomain"].unique().tolist()
        lst_excluded_qualified_names = list(set(lst_unique_qualified_names) - set(lst_included_qualified_names))
        create_default_scan(
            scan_name=scan_name,
            collection_name_unique_id=collection_name_unique_id)
        apply_filter_on_scan(
            scan_name=scan_name,
            lstexcludeUriPrefixes=lst_excluded_qualified_names,
            lstincludeUriPrefixes=lst_included_qualified_names
        )


