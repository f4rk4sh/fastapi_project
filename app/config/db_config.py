from app.config.azure_keyvault_config import AzureKeyVaultConfig


class DBConfig:
    DB_USER = AzureKeyVaultConfig.client.get_secret("DBUser").value
    DB_HOST = AzureKeyVaultConfig.client.get_secret("DBHost").value
    DB_NAME = AzureKeyVaultConfig.client.get_secret("DBName").value
    DB_DRIVER = AzureKeyVaultConfig.client.get_secret("DBDriver").value
    MSSQL_SA_PASSWORD = AzureKeyVaultConfig.client.get_secret("MSSQLSAPassword").value
    MSSQL_TCP_PORT = AzureKeyVaultConfig.client.get_secret("MSSQLTCPPort").value

    SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{MSSQL_SA_PASSWORD}@{DB_HOST}:{MSSQL_TCP_PORT}/{DB_NAME}?driver={DB_DRIVER}"
