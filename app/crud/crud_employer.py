from typing import List

from sqlalchemy import and_

from app.crud.crud_base import CRUDBase, ModelType
from app.db.models import Employer, User
from app.schemas.employer import EmployerCreate, EmployerUpdate
from app.utils.exceptions.common_exceptions import HTTPBadRequestException, HTTPNotFoundException


class CRUDEmployer(CRUDBase[Employer, EmployerCreate, EmployerUpdate]):
    def get_by_attribute(self, **kwargs) -> ModelType:
        filter_user_args = []
        filter_employer_args = []
        for key, value in kwargs.items():
            if hasattr(User, key):
                filter_user_args.append(getattr(User, key) == value)
            else:
                filter_employer_args.append(getattr(self.model, key) == value)
        obj = (
            self.db.query(self.model)
            .join(User)
            .filter(and_(True, *filter_user_args))
            .filter(and_(True, *filter_employer_args))
            .first()
        )
        if isinstance(obj, User):
            if obj.employer:
                return obj.employer
        return obj

    def search_by_parameter(
        self, parameter: str, keyword: str, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        if hasattr(User, parameter):
            filter_arg = getattr(User, parameter)
            users = (
                self.db.query(User)
                .filter(filter_arg.contains(keyword))
                .order_by(User.id)
                .offset(skip)
                .limit(limit)
                .all()
            )
            results = [user.employer for user in users if user.employer]
        elif hasattr(self.model, parameter):
            filter_arg = getattr(self.model, parameter)
            results = (
                self.db.query(self.model)
                .filter(filter_arg.contains(keyword))
                .order_by(self.model.id)
                .offset(skip)
                .limit(limit)
                .all()
            )
        else:
            raise HTTPBadRequestException(detail="Invalid search parameter")
        if not results:
            raise HTTPNotFoundException(self.model.__name__)
        return results


employer: CRUDEmployer = CRUDEmployer(Employer)
