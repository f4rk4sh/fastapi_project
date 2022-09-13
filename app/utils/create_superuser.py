import os
from datetime import datetime

from dotenv import load_dotenv

from app import crud
from app.security.passwords import hash_password

load_dotenv()


def create_superuser():
    role_superuser = crud.role.get_by_attribute(name="superuser")
    status_activated = crud.status_type.get_by_attribute(name="active")
    crud.user.create(
        {
            "email": os.getenv("SU_EMAIL"),
            "phone": os.getenv("SU_PHONE"),
            "password": hash_password(os.getenv("SU_PASSWORD")),
            "creation_date": datetime.utcnow(),
            "activation_date": datetime.utcnow(),
            "role_id": role_superuser.id,
            "status_type_id": status_activated.id,
        }
    )


if __name__ == '__main__':
    create_superuser()
