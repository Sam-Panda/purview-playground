# Metadata Extract from Azure Purview for Reporting


## Objective

In this example, we will try to extract metadata from the Azure Purview service using the REST API. The metadata will be having information about the classification and the associated assets. The extracted metadata will be stored in a CSV file.

## Prerequisites
1. You already have an Azure Purview environment.
2. You have already created a service principal to authenticate to the Microsoft Purview Environment.
3. You have a python virtual environment where the required modules are already installed (requirements.txt).
4. Please follow the steps to [setup the authentication](https://learn.microsoft.com/en-us/purview/tutorial-using-rest-apis).
5. In the Azure Purview environment, you have already registered the Azure SQL DB as a datasource.


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


## Execute the script

Please provide the collection name which you would like to extract the metadata from. The collection name is the name of the collection that you have created in the Purview service. 

```python
# give the child collection name where we have the assets
collection_name = "Marketing"
```

Once the virtual environment is created and the .env file is updated with the correct values, we can execute the script using the following command.
`metadata_extract_for_reporting\metadata_extract.py`

Please note that if you would like to use EntraID authentication,, you can disable the service principal authentication and enable the EntraID authentication in the script. 

```python
def get_credentials():
    # credentials = ClientSecretCredential(client_id=client_id, client_secret=client_secret, tenant_id=tenant_id) # this portion is for service principal authentication
    credentials = AzureCliCredential() # this portion is for EntraID authentication
    return credentials

```

## Deep dive into the Steps of the script
1. We first get the credentials using the get_credentials() function. We can use the service principal or the EntraID authentication to get the credentials.
2. We get the access token using the credentials.
3. We get the collection ID using the collection name.
4. We then get all the metadata from the collection using the GET API call.
5. we then extract out the column information from the metadata where we got the classification and the associated assets.
6. We then write the extracted metadata to a CSV file.

## Output

Here is the Csv file that got created after the script execution.


![alt text](https://github.com/Sam-Panda/purview-playground/blob/main/metadata_extract_for_reporting/.media/CSV_output.png)