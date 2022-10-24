from app.crud.crud_base import CRUDBase
from app.db.models import AccountType
from app.schemas.schema_account_type import AccountTypeCreate, AccountTypeUpdate


class CRUDAccountType(CRUDBase[AccountType, AccountTypeCreate, AccountTypeUpdate]):
    pass


account_type = CRUDAccountType(AccountType)
