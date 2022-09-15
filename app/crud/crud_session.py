from sqlalchemy import and_, desc

from app.crud.crud_base import CRUDBase, ModelType
from app.db.models import Session
from app.schemas.session import SessionCreate, SessionUpdate


class CRUDSession(CRUDBase[Session, SessionCreate, SessionUpdate]):
    def get_one_ordered_by_creation_date(self, **kwargs) -> ModelType:
        filter_args = []
        for key, value in kwargs.items():
            filter_args.append(getattr(self.model, key) == value)
        return self.db.query(self.model).filter(and_(*filter_args)).order_by(desc(self.model.creation_date)).first()


session: CRUDSession = CRUDSession(Session)
