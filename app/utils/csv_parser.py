import csv
import logging
from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Connection
from sqlalchemy import DateTime, Boolean, Date

from app.db import models
from app.db.models import User, Employee, Employer, EmployerType, Role, StatusType, Base
from app.db.session import engine


def insert_basic_data() -> Optional:
    """
    Insert basic database data to newly created tables.
    """
    for source in [__DataSource(table) for table in [
            Role, StatusType, User, EmployerType, Employer, Employee
        ]
    ]:
        _aggregator(source.data_route, source.table)


class __DataSource:
    def __init__(self, table: Base) -> Optional:
        self.table: Base = table
        self.data_route: str = f"app/db/data/{table.__name__}.csv"


class __DbAggregate:
    """
    Aggregate from csv file and insert data to passed newly created table
    """
    __bind: Connection = engine
    __session: Session = Session(bind=__bind)

    @classmethod
    def __convert_column_detail(cls, column_name: str, column_type: any, data: str) -> (str, datetime):
        if isinstance(column_type, Date):
            return column_name, datetime.strptime(data, "%Y-%m-%d").date() if data else None
        if isinstance(column_type, DateTime):
            return column_name, datetime.strptime(data, "%Y-%m-%d %H:%M:%S.%f") if data else None
        if isinstance(column_type, Boolean):
            return column_name, True if data == "true" else False if data == "false" else None
        return column_name, data if data else None

    @classmethod
    def __convert_rows_details(cls, rows_details: list) -> List:
        return [
            cls.__convert_column_detail(column_detail["key"], column_detail["type"], column_data)
            for column_detail, column_data in rows_details
        ]

    @classmethod
    def __get_csv_data(cls, data_file_path: str, table: Base) -> List[list]:
        columns: List[dict] = [{"key": column.key, "type": column.type} for column in table.__table__.columns]

        with open(data_file_path) as csv_file:
            return [
                table(**dict(cls.__convert_rows_details(list(zip(columns, row)))))
                for row in csv.reader(csv_file, delimiter=",")
            ]

    def __call__(self, data_file_path: str, table: Base) -> Optional:
        try:
            data: [Base] = self.__get_csv_data(data_file_path, table)
            self.__session.add_all(data)
            self.__session.commit()
        except Exception as exc:
            logging.exception(table.__name__, exc)
            self.__session.rollback()


_aggregator: __DbAggregate = __DbAggregate()

if __name__ == '__main__':
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    insert_basic_data()
