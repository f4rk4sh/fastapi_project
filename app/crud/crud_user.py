from typing import Optional

from app.crud.crud_base import CRUDBase, ModelType
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.exceptions.common_exceptions import HTTPBadRequestException
from app.security.passwords import verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def authenticate(self, email: str, password: str) -> Optional[ModelType]:
        _user = self.get_by_attribute(email=email)
        if _user:
            if verify_password(password, _user.password):
                return _user
        raise HTTPBadRequestException(detail="Incorrect email or password")


user: CRUDUser = CRUDUser(User)
