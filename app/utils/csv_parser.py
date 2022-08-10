import csv
import sys
from datetime import datetime, date

from sqlalchemy.orm import Session

from app.db.models import User, Employee, Employer, EmployerType, Role, StatusType
from app.db.get_database import get_db

db: Session = next(get_db())


def parsing(file_path: str):
    models_dict = {
        "employer.csv": Employer,
        "employee.csv": Employee,
        "employer_type.csv": EmployerType,
        "status_type.csv": StatusType,
        "role.csv": Role

    }
    file_name = file_path.split("/")[-1].lower()
    Model = models_dict[file_name]
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        if Model == Employee or Model == Employer:
            for data in csv_reader:
                user_dict = dict(
                    email=data["email"],
                    phone=data["phone"],
                    role_id=data["role_id"],
                    status_type_id=data["status_type_id"]
                )
                user = User(**user_dict)
                user.creation_date = datetime.utcnow()
                db.add(user)
                db.flush()
                if Model == Employee:
                    info_dict = dict(
                        fullname=data["fullname"],
                        passport=data["passport"],
                        tax_id=data["tax_id"],
                        birth_date=date(*[int(i) for i in (data["birth_date"].split("/"))]),
                        user_id=user.id,
                        employer_id=data["employer_id"]
                    )
                else:
                    info_dict = dict(
                        address=data["address"],
                        edrpou=data["edrpou"],
                        expire_contract_date=date(*[int(i) for i in (data["expire_contract_date"].split("/"))]),
                        salary_date=date(*[int(i) for i in (data["salary_date"].split("/"))]),
                        prepayment_date=date(*[int(i) for i in (data["prepayment_date"].split("/"))]),
                        user_id=user.id,
                        employer_type_id=data["employer_type_id"]
                    )
                obj = Model(**info_dict)
                db.add(obj)
                db.commit()
        else:
            for data in csv_reader:
                obj = Model(**data)
                db.add(obj)
                db.commit()


if __name__ == '__main__':
    parsing(sys.argv[1])
