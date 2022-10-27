from datetime import datetime

from app.crud.crud_bank import CRUDBank, bank as bank_crud
from app.db.models import Bank, Session
from app.manager.manager_base import ManagerBase, ModelType
from app.schemas.schema_bank import BankCreate, BankUpdate


class BankManager(ManagerBase[Bank, CRUDBank, BankCreate, BankUpdate]):
    def create(self, obj_in: BankCreate, session: Session) -> ModelType:
        obj_in_data = obj_in.dict()
        obj_in_data.update(
            {
                "creation_date": datetime.utcnow(),
                "is_active": True,
            }
        )
        return self.crud.create(obj_in_data)


bank: BankManager = BankManager(bank_crud)
