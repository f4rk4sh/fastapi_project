from app.crud.crud_base import CRUDBase
from app.db.models import Session
from app.schemas.session import SessionCreate, SessionUpdate


class CRUDSession(CRUDBase[Session, SessionCreate, SessionUpdate]):
    pass


session: CRUDSession = CRUDSession(Session)
