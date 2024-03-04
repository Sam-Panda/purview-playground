# Scoped Scanning of the datasource using the Purview rest API.


## Objective

In this example, we will explore automating the scope scanning of the datasource (e.g., Azure SQL DB) using REST API. We will utilize a lookup list (CSV file) to specify the scan's scope, as manually selecting objects from the Purview UI can be challenging.

## Prerequisites
1. You already have an Azure Purview environment.
2. You have already created a service principal to authenticate to the Microsoft Purview Environment.
3. You have a python virtual environment where the required modules are already installed (requirements.txt).
4. Please follow the steps to [setup the authentication](https://learn.microsoft.com/en-us/purview/tutorial-using-rest-apis).
5. In the Azure Purview environment, you have already registered the Azure SQL DB as a datasource.

## Create the Lookup scope list

In this example, we will scan the Azure SQL DB, specifically using the WorldWideImports database. First, we must create a lookup table containing all possible objects. This is necessary for the payload sent to the Purview service. For the scope scanning, the payload requires an include list and exclude list. For instance, to scan the _WorldWideImports.Sales.SalesOrder_ object, we must include following it in the include list and exclude everything else in the exclude list. 


* mssql:/sql-svr-name.database.windows.net/WideWorldImporters/
* mssql:/sql-svr-name.database.windows.net/WideWorldImporters/Sales
* mssql:/sql-svr-name.database.windows.net/WideWorldImporters/Sales/SalesOrder

You can create the list using the script (`data_source_scanning\utilities\scoped_scanning_sql_db_query.sql`). Keep the lookup list in the following path (`data_source_scanning\InputFiles\assestsToBeScanned.csv`).

The objects that you would like to include, you can populate the corresponding collection name and associated scan name in the respective columns. For the other objects which we don't want to be included in the scan, we can put "exclude". Here is how the list look like

![alt text](https://github.com/Sam-Panda/purview-playground/blob/f40ef09c8a21b34c1449df979fcd64d3b2145bc2/data_source_scanning/.media/assets_to_be_inlcuded.png)

## create the python virtual environment 

In order to execute the script, we need to [create a python virtual environment](https://docs.python.org/3/library/venv.html) where we can install all the required modules from the requirement.txt file. 
`python -m venv <virtual_environmnet_name>`

## .env file.
.env file contains all the configuration values that is needed to execute the script. 
* CLIENT_ID= _Client ID of the service Principal_ 
* CLIENT_SECRET= _client secret of the the service Principal_
* TENANT_ID= _Tenant ID_
* PURVIEW_ACCOUNT_NAME= _Purview Account Name_
* SUBSCRIPTION_ID= _Subscription ID_
* RESOURCE_ENDPOINT= _"SQL_Server_Name.database.windows.net". This is specific to the current scenario as we are scanning the Azure SQL DB._
* DATABASE_NAME = _Azure SQL DB Name_
* PURVIEW_REGISTERED_DATASOURCE_NAME = _The data source that is registered in the Purview account for the Azure SQL DB._

## Execute the script

Once the virtual environment is created and the .env file is updated with the correct values, we can execute the script using the following command.
`python data_source_scanning\scoped_scanning_from_lookup_file.py`

Please note that if you would like to use EntraID authentication,, you can disable the service principal authentication and enable the EntraID authentication in the script. 

```python
def get_credentials():
    # credentials = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id) # this portion is for service principal authentication
    credentials = AzureCliCredential() # this portion is for EntraID authentication
    return credentials

```

## Output

After running the script, we would be able to see the output in the console. If we go to the Purview service, we would be able to see the scoped scanning job in the "Scanning" tab.

![alt text](https://github.com/Sam-Panda/purview-playground/blob/f40ef09c8a21b34c1449df979fcd64d3b2145bc2/data_source_scanning/.media/scopped_scanning_image.png
