import csv
import logging
from datetime import datetime

from sqlalchemy import Date, DateTime, Boolean
from sqlalchemy.orm import Session

from app.db import models
from app.db.models import User, Employee, Employer, EmployerType, Role, StatusType
from app.db.get_database import get_db
from app.db.session import engine

db: Session = next(get_db())


def parsing():
    for model in [Role, StatusType,  EmployerType, User, Employer, Employee]:
        file_path = f"app/db/data/{model.__name__}.csv"
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            header = csv_reader.fieldnames
            column_types = {column.key: column.type for column in model.__table__.columns if column.key in header}
            for data in csv_reader:
                converted_data = convert_data_types(column_types, data)
                obj = model(**converted_data)
                db.add(obj)
                try:
                    db.commit()
                except Exception as exc:
                    logging.exception(exc)
                    db.rollback()


def convert_data_types(column_types: dict, data: dict):
    for key, value in data.items():
        if isinstance(column_types[key], Date):
            data[key] = datetime.strptime(value, "%Y-%m-%d").date()
            continue
        if isinstance(column_types[key], DateTime):
            data[key] = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
            continue
        if isinstance(column_types[key], Boolean):
            data[key] = True if value == "true" else False
            continue
    return data


if __name__ == '__main__':
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    parsing()
