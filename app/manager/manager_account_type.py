from app.crud.crud_account_type import CRUDAccountType
from app.crud.crud_account_type import account_type as crud_account_type
from app.db.models import AccountType
from app.manager.manager_base import ManagerBase
from app.schemas.schema_account_type import (AccountTypeCreate,
                                             AccountTypeUpdate)


class AccountTypeManager(
    ManagerBase[AccountType, CRUDAccountType, AccountTypeCreate, AccountTypeUpdate]
):
    pass


account_type: AccountTypeManager = AccountTypeManager(crud_account_type)
