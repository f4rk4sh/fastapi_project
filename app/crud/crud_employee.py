from typing import List

from sqlalchemy import and_

from app.utils.exceptions.common_exceptions import HTTPBadRequestException, HTTPNotFoundException
from app.crud.crud_base import CRUDBase, ModelType
from app.db.models import Employee, User
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


class CRUDEmployee(CRUDBase[Employee, EmployeeCreate, EmployeeUpdate]):
    def get_by_attribute(self, **kwargs) -> ModelType:
        filter_user_args = []
        filter_employee_args = []
        for key, value in kwargs.items():
            if hasattr(User, key):
                filter_user_args.append(getattr(User, key) == value)
            else:
                filter_employee_args.append(getattr(self.model, key) == value)
        obj = (
            self.db.query(self.model)
            .join(User)
            .filter(and_(*filter_user_args))
            .filter(and_(*filter_employee_args))
            .first()
        )
        if isinstance(obj, User):
            if obj.employee:
                return obj.employee
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
            results = [user.employee for user in users if user.employee]
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


employee: CRUDEmployee = CRUDEmployee(Employee)
