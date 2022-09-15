import os

from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from dotenv import load_dotenv


load_dotenv()


class AzureKeyVaultConfig:
    _AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
    _AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
    _AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
    _AZURE_KEYVAULT_NAME = os.getenv("AZURE_KEYVAULT_NAME")
    _AZURE_KEYVAULT_URI = f"https://{_AZURE_KEYVAULT_NAME}.vault.azure.net/"

    _credential = ClientSecretCredential(
            tenant_id=_AZURE_TENANT_ID,
            client_id=_AZURE_CLIENT_ID,
            client_secret=_AZURE_CLIENT_SECRET,
        )

    client = SecretClient(
            vault_url=_AZURE_KEYVAULT_URI, credential=_credential
        )