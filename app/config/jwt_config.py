import os

from dotenv import load_dotenv

load_dotenv()


class JWTConfig:
    JWT_SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_TOKEN_EXPIRE_TIME = os.getenv("JWT_TOKEN_EXPIRE_TIME")
