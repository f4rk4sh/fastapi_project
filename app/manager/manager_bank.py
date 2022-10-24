from app.crud.crud_bank import CRUDBank, bank as bank_crud
from app.db.models import Bank
from app.manager.manager_base import ManagerBase
from app.schemas.schema_bank import BankCreate, BankUpdate


class BankManager(ManagerBase[Bank, CRUDBank, BankCreate, BankUpdate]):
    pass


bank: BankManager = BankManager(bank_crud)
