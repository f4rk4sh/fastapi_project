from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config.db_config import DBConfig

# for local connection

SQLALCHEMY_DATABASE_URL = \
    f"mssql+pyodbc://{DBConfig.DB_USER_LOCAL}:{DBConfig.DB_PASSWORD_LOCAL}@{DBConfig.DB_HOST_LOCAL}:{DBConfig.DB_PORT_LOCAL}/db?driver={DBConfig.DB_DRIVER}"

# for docker connection

# SQLALCHEMY_DATABASE_URL = \
#      f"mssql+pyodbc://{DBConfig.DB_USER}:{DBConfig.DB_PASSWORD}@{DBConfig.DB_HOST}:{DBConfig.DB_PORT}/{DBConfig.DB_NAME}?driver={DBConfig.DB_DRIVER}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
