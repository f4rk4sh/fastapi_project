import csv
import logging
from datetime import datetime

from sqlalchemy import Boolean, Date, DateTime
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.db.models import Employee, Employer, EmployerType, Role, StatusType, User


def parsing(session: Session = next(get_session())):
    for model in [Role, StatusType, EmployerType, User, Employer, Employee]:
        file_path = f"/src/app/db/data/{model.__name__}.csv"
        with open(file_path, "r") as csv_file:
            csv_reader = csv.DictReader(csv_file)
            column_types = {
                column.key: column.type for column in model.__table__.columns
            }
            for data in csv_reader:
                converted_data = convert_data_types(column_types, data)
                obj = model(**converted_data)
                session.add(obj)
                try:
                    session.commit()
                except Exception as exc:
                    logging.exception(exc)
                    session.rollback()


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


if __name__ == "__main__":
    parsing()
