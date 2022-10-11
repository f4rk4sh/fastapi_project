from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class DBConfig(BaseSettings):
    DB_USER: str
    DB_HOST: str
    DB_NAME: str
    DB_DRIVER: str
    DB_PASSWORD: str = Field(..., env="MSSQL_SA_PASSWORD")
    DB_PORT: str = Field(..., env="MSSQL_TCP_PORT")
    DB_HOST_LOCAL: str
    DB_PORT_LOCAL: str
    DB_NAME_TEST: str


db_cfg = DBConfig()
