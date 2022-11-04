from typing import List

from app.crud.crud_payment_history import CRUDPaymentHistory, payment_history as crud_payment_history
from app.db.models import PaymentHistory, Session
from app.manager.manager_abstract import CRUDType, ManagerAbstract, ModelType
from app.schemas.schema_payment_history import PaymentHistoryCreate, PaymentHistoryUpdate


class PaymentHistoryManager(
    ManagerAbstract[
        PaymentHistory,
        CRUDPaymentHistory,
        PaymentHistoryCreate,
        PaymentHistoryUpdate
    ]
):
    def __init__(self, crud: CRUDType):
        self.crud = crud

    def fetch_one(self, obj_id: int, session: Session) -> ModelType:
        return self.crud.get(obj_id)

    def fetch_all(self, session: Session) -> List[ModelType]:
        return self.crud.get_multi()

    def search(
        self, parameter: str, keyword: str, max_results: int, session: Session
    ) -> List[ModelType]:
        return self.crud.search_by_parameter(parameter, keyword, max_results)


payment_history: PaymentHistoryManager = PaymentHistoryManager(crud_payment_history)
