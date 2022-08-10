import csv
import sys
from datetime import datetime, date

from sqlalchemy.orm import Session

from app.db.get_database import get_db
from app.db.models import User, Employee

# csv file columns
#
# fullname|passport|tax_id|birth_date|employer_id|email|phone|role_id|status_type_id
#
# csv file example
#
# John Doe,MM123456,12345678,1999/1/1,1,example@mail.com,+380123456789,1,1

db: Session = next(get_db())


def parsing(file: str):
    with open(file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for employee_data in csv_reader:
            user_dict = dict(
                email=employee_data[5],
                phone=employee_data[6],
                role_id=employee_data[7],
                status_type_id=employee_data[8]
            )
            user = User(**user_dict)
            user.creation_date = datetime.utcnow()
            db.add(user)
            db.flush()
            employee_dict = dict(
                fullname=employee_data[0],
                passport=employee_data[1],
                tax_id=employee_data[2],
                birth_date=date(*[int(i) for i in (employee_data[3].split("/"))]),
                user_id=user.id,
                employer_id=employee_data[4]
            )
            employee = Employee(**employee_dict)
            db.add(employee)
            db.commit()

# to run inside "pre_start.sh" use command "python ./app/utils/csv_parser.py ./app/utils/example.csv"
#
# if __name__ == '__main__':
#     parsing(sys.argv[1])
