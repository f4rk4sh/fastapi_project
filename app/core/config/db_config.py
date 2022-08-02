import os
from dotenv import load_dotenv

load_dotenv()


class DBConfig(object):
    DB_USER = str(os.getenv('DB_USER'))
    DB_PASSWORD = str(os.getenv('SA_PASSWORD'))
    DB_HOST = str(os.getenv('DB_HOST'))
    DB_PORT = int(os.getenv('DB_PORT'))
    DB_NAME = str(os.getenv('DB_NAME'))
    DB_DRIVER = str(os.getenv('DB_DRIVER'))
    DB_USER_LOCAL = str(os.getenv('DB_USER_LOCAL'))
    DB_PASSWORD_LOCAL = str(os.getenv('DB_PASSWORD_LOCAL'))
    DB_HOST_LOCAL = str(os.getenv('DB_HOST_LOCAL'))
    DB_PORT_LOCAL = int(os.getenv('DB_PORT_LOCAL'))
