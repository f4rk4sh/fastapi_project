from datetime import datetime

from app.crud.crud_bank import CRUDBank
from app.crud.crud_bank import bank as bank_crud
from app.db.models import Bank, Session
from app.manager.manager_abstract import ModelType
from app.manager.manager_base import ManagerBase
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
