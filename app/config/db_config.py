import os

from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    DB_USER = os.getenv("DB_USER")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_DRIVER = os.getenv("DB_DRIVER")
    MSSQL_SA_PASSWORD = os.getenv("MSSQL_SA_PASSWORD")
    MSSQL_TCP_PORT = os.getenv("MSSQL_TCP_PORT")

    SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{MSSQL_SA_PASSWORD}@{DB_HOST}:{MSSQL_TCP_PORT}/{DB_NAME}?driver={DB_DRIVER}"

    DB_HOST_LOCAL = os.getenv("DB_HOST_LOCAL")
    DB_PORT_LOCAL = os.getenv("DB_PORT_LOCAL")

    SQLALCHEMY_DATABASE_URL_LOCAL = f"mssql+pyodbc://{DB_USER}:{MSSQL_SA_PASSWORD}@{DB_HOST_LOCAL}:{DB_PORT_LOCAL}/db?driver={DB_DRIVER}"
