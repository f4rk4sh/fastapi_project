from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME, DB_DRIVER,\
    DB_USER_LOCAL, DB_PASSWORD_LOCAL, DB_HOST_LOCAL, DB_PORT_LOCAL

# for local connection

SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{DB_USER_LOCAL}:{DB_PASSWORD_LOCAL}@{DB_HOST_LOCAL}:{DB_PORT_LOCAL}/db?driver={DB_DRIVER}"
# SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://admin:123@LWO1-LHP-A00359:1434/db?driver=SQL+Server"


# for docker connection

# SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?driver={DB_DRIVER}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
