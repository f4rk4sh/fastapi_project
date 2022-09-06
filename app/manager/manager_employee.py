from datetime import datetime

from fastapi import Response, status

from app import crud
from app.crud.crud_employee import CRUDEmployee
from app.db.models import Employee
from app.manager.manager_base import ManagerBase, ModelType
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.utils.exceptions.common_exceptions import HTTPBadRequestException
from app.utils.security import hash_password


class EmployeeManager(
    ManagerBase[Employee, CRUDEmployee, EmployeeCreate, EmployeeUpdate]
):
    def create(self, obj_in: EmployeeCreate) -> ModelType:
        if crud.user.get_by_attribute(email=obj_in.user.email):
            raise HTTPBadRequestException(
                detail="Account with this email already exists"
            )
        role_employee = crud.role.get_by_attribute(name="employee")
        status_not_activated = crud.status_type.get_by_attribute(name="not active")
        obj_in_data = obj_in.dict()
        user_data = obj_in_data.pop("user")
        user_data.update(
            {
                "creation_date": datetime.utcnow(),
                "password": hash_password(obj_in.user.password),
                "role_id": role_employee.id,
                "status_type_id": status_not_activated.id,
            }
        )
        user = crud.user.create(user_data, is_flush=True)
        obj_in_data["user_id"] = user.id
        return self.executor.create(obj_in_data)

    def update(self, obj_in: EmployeeUpdate) -> ModelType:
        obj = self.executor.get(obj_in.id)
        user = crud.user.get_by_attribute(email=obj_in.user.email)
        if user:
            if obj.user_id != user.id:
                raise HTTPBadRequestException(
                    detail="Account with this email already exists"
                )
        user = crud.user.get(obj.user_id)
        crud.user.update(user, obj_in.user, is_flush=True)
        return self.executor.update(obj, obj_in)

    def delete(self, id: int) -> Response:
        obj = self.executor.get(id)
        crud.user.delete(obj.user_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


employee: EmployeeManager = EmployeeManager(Employee, CRUDEmployee)
