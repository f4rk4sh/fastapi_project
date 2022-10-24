from app.crud.crud_base import CRUDBase
from app.db.models import Bank
from app.schemas.schema_bank import BankCreate, BankUpdate


class CRUDBank(CRUDBase[Bank, BankCreate, BankUpdate]):
    pass


bank = CRUDBank(Bank)
