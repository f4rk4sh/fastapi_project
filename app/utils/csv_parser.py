import csv
import logging
from datetime import datetime

from sqlalchemy import Boolean, Date, DateTime
from sqlalchemy.orm import Session

from app.db.get_database import get_db
from app.db.models import (AccountType, Bank, Employee, EmployeeAccount, Employer,
                           EmployerType, EmployerPaymentMethod, PaymentHistory,
                           PaymentStatusType, Role, StatusType, User)


def parsing(db: Session = next(get_db())) -> None:
    for model in [
        Role,
        StatusType,
        User,
        EmployerType,
        Employer,
        Bank,
        EmployerPaymentMethod,
        Employee,
        AccountType,
        EmployeeAccount,
        PaymentStatusType,
        PaymentHistory,
    ]:
        with open(f"app/db/data/{model.__name__}.csv", "r") as csv_file:
            column_types = {
                column.key: column.type for column in model.__table__.columns
            }
            for data in csv.DictReader(csv_file):
                converted_data = convert_data_types(column_types, data)
                obj = model(**converted_data)
                db.add(obj)
                try:
                    db.commit()
                except Exception as exc:
                    logging.exception(exc)
                    db.rollback()


def convert_data_types(column_types: dict, data: dict) -> dict:
    for key, value in data.items():
        if isinstance(column_types[key], Date):
            data[key] = datetime.strptime(value, "%Y-%m-%d").date()
            continue
        if isinstance(column_types[key], DateTime):
            data[key] = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
            continue
        if isinstance(column_types[key], Boolean):
            data[key] = True if value == 'true' else False
            continue
    return data


if __name__ == "__main__":
    parsing()
