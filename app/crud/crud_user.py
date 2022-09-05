from app.crud.crud_base import CRUDBase
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass


user: CRUDUser = CRUDUser(User)
