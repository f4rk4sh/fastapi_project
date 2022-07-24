# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session

# SQLALCHEMY_DATABASE_URL = "mssql+pyodbc://scott:tiger@mydsn"
# # SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# engine = create_engine(
#     "mssql+pyodbc://SA:password123!@127.0.0.1:1433/db?driver=SQL+Server"
# )
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()


# class Item(Base):
#     __tablename__ = "Items"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
