import os
from datetime import datetime

from dotenv import load_dotenv

from app import crud
from app.constansts.constants_role import ConstantRole
from app.constansts.constants_status_type import ConstantStatusType
from app.security.passwords import hash_password

load_dotenv()


def create_superuser():
    role_su = crud.role.get_by_attribute(name=ConstantRole.su)
    status_active = crud.status_type.get_by_attribute(name=ConstantStatusType.active)
    crud.user.create(
        {
            "email": os.getenv("SU_EMAIL"),
            "phone": os.getenv("SU_PHONE"),
            "password": hash_password(os.getenv("SU_PASSWORD")),
            "creation_date": datetime.utcnow(),
            "activation_date": datetime.utcnow(),
            "role_id": role_su.id,
            "status_type_id": status_active.id,
        }
    )


if __name__ == '__main__':
    create_superuser()
