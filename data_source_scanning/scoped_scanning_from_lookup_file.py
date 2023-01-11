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

#declare variables 

datasource_name = "ds4mapi_azuresqlserver_opnhckdasqlsvr"
resource_endpoint = "opnhckdasqlsvr.database.windows.net"
resource_id = f"/subscriptions/{subscription_id}/resourceGroups/openhack_data_analytics/providers/Microsoft.Sql/servers/opnhckdasqlsvr"
reference_name_purview = purview_account_name
databaseName = "opnhckdasqldb"



def get_collection_Id(collection_name):
    try:
        client = i.get_admin_client()
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
            "kind": "AzureSqlDatabaseMsi",
            "properties": {

                "collection": {
                    "type": "CollectionReference",
                    "referenceName": collection_name_unique_id
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

def apply_filter_on_scan(scan_name, lstexcludeUriPrefixes, lstincludeUriPrefixes):
    
    try:
        client = i.get_purview_client()
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
    client.filters.create_or_update(data_source_name=datasource_name, scan_name=scan_name, body=filter_body_input)




# read the csv files
file_path = os.path.join(os.getcwd(),"InputFiles", "assestsToBeScanned.csv")
df_csv = pd.read_csv(file_path)
unique_scan_names = df_csv["scanName"].unique()
for scan_name in unique_scan_names:
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


