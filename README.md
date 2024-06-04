# purview-playground

## How to use the Azure Purview REST API and automate CRUD operations

**Example 1**: [Scoped Scanning of the datasource using the Purview rest API.](https://github.com/Sam-Panda/purview-playground/blob/main/data_source_scanning)

**Example 2**: [Metadata Extract from Azure Purview for Reporting.](https://github.com/Sam-Panda/purview-playground/blob/main/metadata_extract_for_reporting)

**Example 3**: [Update Metadata in Azure Purview.](https://github.com/Sam-Panda/purview-playground/tree/main/create_update_metadata)

## A guide for developers who want to leverage the Azure Purview REST API to create, read, update and delete Purview resources.
### Introduction
Azure Purview is a unified data governance service that helps you manage and govern your on-premises, multicloud, and software-as-a-service (SaaS) data. It enables you to create a holistic, up-to-date map of your data landscape with automated data discovery, sensitive data classification, and end-to-end data lineage. It also empowers you to control data access and usage with policies, data cataloging, and insights.

One of the features of Azure Purview is the REST API, which allows you to programmatically interact with Purview resources and perform various operations. In this blog post, we will show you how to use the Azure Purview REST API and automate different CRUD (create, read, update and delete) operations in Purview. We will cover the following topics:

* How to authenticate and authorize your requests to the Purview REST API.
* How to create the required payload for the CRUD operations.
* How to find the required payload for the REST API call.

### Prerequisites

Before you can use the Azure Purview REST API, you need to have the following:

* An Azure subscription. If you don't have one, you can create one for free undefined.
* An EntraID tenant. If you don't have one, you can create one for free undefined.
* An Azure Purview resource. [Steps](https://learn.microsoft.com/en-us/purview/create-microsoft-purview-portal).
* An AAD application with the appropriate permissions to access the Purview REST API. You can follow the steps undefined to create and configure an AAD application for Purview. Here is the [tutorial](https://learn.microsoft.com/en-us/purview/tutorial-using-rest-apis) for the authentication.
* A python virtual environment which will have all the required modules pre-installed.

### Creating payload json
In Azure Purview, we perform different actions with different combinations. How can we find the actual payload that needs to be submitted via the REST API?  
We have the REST API references documented [here](https://learn.microsoft.com/en-us/rest/api/purview/?view=rest-purview-scanningdataplane-2023-09-01).

I generally find the UI is the easiest way to find the required payload that is needed for the REST API call. For example, lets talk about the use case where we would like to automate the scoped scanning for the Azure SQL DB.  Lets perform the same activity first in the UI, and from the DevTools (press F12 in Edge browser) monitor the request that is being sent to the Purview Service.

Here are the manual steps that we perform in the UI:

 ![alt text](https://github.com/Sam-Panda/purview-playground/blob/main/.media/manualstepsUIimage.png)

The equivalent request that we get from the devtools. 

 ![alt text](https://github.com/Sam-Panda/purview-playground/blob/main/.media/devtools1.png)
 
 ![alt text](https://github.com/Sam-Panda/purview-playground/blob/main/.media/devtools2image.png)

Here is the code reference for the same to build the payload. 

```python


{
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

```
``` python
    filter_body_input = {
    "properties":{
        "excludeUriPrefixes":lstexcludeUriPrefixes,
        "includeUriPrefixes":lstincludeUriPrefixes,
        "excludeRegexes":None,
        "includeRegexes":None
        }
     }

```