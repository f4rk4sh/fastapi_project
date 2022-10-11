import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.config.su_config import su_cfg
from app.constansts.constants_role import ConstantRole
from app.constansts.constants_status_type import ConstantStatusType
from app.db.get_database import get_db
from app.db.models import Role, StatusType, User
from app.security.passwords import hash_password


def create_superuser(db: Session = next(get_db())):
    role_su = db.query(Role).filter(Role.name == ConstantRole.su).first()
    status_active = db.query(StatusType).filter(StatusType.name == ConstantStatusType.active).first()
    su = User(
        email=su_cfg.SU_EMAIL,
        phone=su_cfg.SU_PHONE,
        password=hash_password(su_cfg.SU_PASSWORD),
        creation_date=datetime.utcnow(),
        activation_date=datetime.utcnow(),
        role_id=role_su.id,
        status_type_id=status_active.id,
    )
    db.add(su)
    try:
        db.commit()
    except Exception as exc:
        logging.exception(exc)
        db.rollback()


if __name__ == '__main__':
    create_superuser()
