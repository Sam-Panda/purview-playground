from azure.purview.scanning import PurviewScanningClient
from azure.purview.catalog import PurviewCatalogClient
from azure.purview.administration.account import PurviewAccountClient
from azure.identity import ClientSecretCredential 
from azure.core.exceptions import HttpResponseError
import os
from dotenv import load_dotenv

class Intialization:

    def __init__(self):
        load_dotenv()
        # reading the variables from .env file
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.tenant_id = os.getenv("TENANT_ID")
        self.reference_name_purview = os.getenv("PURVIEW_ACCOUNT_NAME")
        self.subscription_id = os.getenv("SUBSCRIPTION_ID")


    def get_credentials(self):
        credentials = ClientSecretCredential(client_id=self.client_id, client_secret=self.client_secret, tenant_id=self.tenant_id)
        return credentials

    def get_purview_client(self):
        credentials = self.get_credentials()
        client = PurviewScanningClient(endpoint=f"https://{self.reference_name_purview}.scan.purview.azure.com", credential=credentials, logging_enable=True)  
        return client

    def get_catalog_client(self):
        credentials = self.get_credentials()
        client = PurviewCatalogClient(endpoint=f"https://{self.reference_name_purview}.purview.azure.com/", credential=credentials, logging_enable=True)
        return client

    def get_admin_client(self):
        credentials = self.get_credentials()
        client = PurviewAccountClient(endpoint=f"https://{self.reference_name_purview}.purview.azure.com/", credential=credentials, logging_enable=True)
        return client
