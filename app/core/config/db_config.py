import os
from dotenv import load_dotenv

load_dotenv()


class DBConfig:
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('SA_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_DRIVER = os.getenv('DB_DRIVER')
    DB_USER_LOCAL = os.getenv('DB_USER_LOCAL')
    DB_PASSWORD_LOCAL = os.getenv('DB_PASSWORD_LOCAL')
    DB_HOST_LOCAL = os.getenv('DB_HOST_LOCAL')
    DB_PORT_LOCAL = os.getenv('DB_PORT_LOCAL')
