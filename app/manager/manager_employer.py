from datetime import datetime

from fastapi import Response, status

from app import crud
from app.constansts.constants_role import ConstantRole
from app.constansts.constants_status_type import ConstantStatusType
from app.crud.crud_employer import CRUDEmployer
from app.db.models import Employer
from app.manager.manager_base import ManagerBase, ModelType
from app.schemas.employer import EmployerCreate, EmployerUpdate
from app.utils.exceptions.common_exceptions import HTTPBadRequestException
from app.security.passwords import hash_password


class EmployerManager(
    ManagerBase[Employer, CRUDEmployer, EmployerCreate, EmployerUpdate]
):
    def create(self, obj_in: EmployerCreate) -> ModelType:
        if crud.user.get_by_attribute(email=obj_in.user.email):
            raise HTTPBadRequestException(
                detail="Account with this email already exists"
            )
        role_employer = crud.role.get_by_attribute(name=ConstantRole.employer)
        status_inactive = crud.status_type.get_by_attribute(name=ConstantStatusType.inactive)
        obj_in_data = obj_in.dict()
        user_data = obj_in_data.pop("user")
        user_data.update(
            {
                "creation_date": datetime.utcnow(),
                "password": hash_password(obj_in.user.password),
                "role_id": role_employer.id,
                "status_type_id": status_inactive.id,
            }
        )
        user = crud.user.create(user_data, is_flush=True)
        obj_in_data["user_id"] = user.id
        return self.executor.create(obj_in_data)

    def update(self, obj_in: EmployerUpdate) -> ModelType:
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


employer: EmployerManager = EmployerManager(Employer, CRUDEmployer)
