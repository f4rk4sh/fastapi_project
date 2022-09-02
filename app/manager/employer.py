from datetime import datetime

from fastapi import Response, status

from app import crud
from app.core.exceptions.common_exceptions import HTTPBadRequestException
from app.core.security import hash_password
from app.schemas.employer import EmployerCreate, EmployerUpdate


class EmployerManager:
    @classmethod
    def fetch_one(cls, id: int):
        return crud.employer.get(id)

    @classmethod
    def fetch_all(cls):
        return crud.employer.get_multi()

    @classmethod
    def search(cls, parameter: str, keyword: str, max_results: int = 100):
        return crud.employer.search_by_parameter(parameter, keyword, max_results)

    @classmethod
    def create(cls, obj_in: EmployerCreate):
        if crud.user.get_by_attribute(email=obj_in.user.email):
            raise HTTPBadRequestException(detail="Account with this email already exists")
        role_employer = crud.role.get_by_attribute(name="employer")
        status_not_activated = crud.status_type.get_by_attribute(name="not active")
        obj_in_data = obj_in.dict()
        user_data = obj_in_data.pop("user")
        user_data.update(
            {
                "creation_date": datetime.utcnow(),
                "password": hash_password(obj_in.user.password),
                "role_id": role_employer.id,
                "status_type_id": status_not_activated.id
             }
        )
        user = crud.user.create(user_data, is_flush=True)
        obj_in_data["user_id"] = user.id
        return crud.employer.create(obj_in_data)

    @classmethod
    def update(cls, obj_in: EmployerUpdate):
        employer = crud.employer.get(obj_in.id)
        user = crud.user.get_by_attribute(email=obj_in.user.email)
        if user:
            if employer.user_id != user.id:
                raise HTTPBadRequestException(detail="Account with this email already exists")
        user = crud.user.get(employer.user_id)
        crud.user.update(user, obj_in.user, is_flush=True)
        return crud.employer.update(employer, obj_in)

    @classmethod
    def delete(cls, id: int):
        employer = crud.employer.get(id)
        crud.user.delete(employer.user_id, is_flush=True)
        crud.employer.delete(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


employer_manager: EmployerManager = EmployerManager()
