import logging
from datetime import datetime

from sqlalchemy.orm import Session

from app.config.superuser_config import superuser_cfg
from app.constansts.constants_role import ConstantRole
from app.constansts.constants_status_type import ConstantStatusType
from app.db.session import get_session
from app.db.models import Role, StatusType, User
from app.security.passwords import hash_password


def create_superuser(session: Session = next(get_session())):
    role_su = session.query(Role).filter(Role.name == ConstantRole.su).first()
    status_active = session.query(StatusType).filter(StatusType.name == ConstantStatusType.active).first()
    su = User(
        email=superuser_cfg.SU_EMAIL,
        phone=superuser_cfg.SU_PHONE,
        password=hash_password(superuser_cfg.SU_PASSWORD),
        creation_date=datetime.utcnow(),
        activation_date=datetime.utcnow(),
        role_id=role_su.id,
        status_type_id=status_active.id,
    )
    session.add(su)
    try:
        session.commit()
    except Exception as exc:
        logging.exception(exc)
        session.rollback()


if __name__ == '__main__':
    create_superuser()
