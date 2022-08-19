from fastapi_utils.inferring_router import InferringRouter
from fastapi import status, Depends, Response

from app import crud
from app.core.exceptions.exception_route_handler import ExceptionRouteHandler
from app.schemas.employer_type import EmployerTypesResponse, EmployerTypeSearch, EmployerTypeCreate, \
    EmployerTypeResponse, EmployerTypeUpdate, EmployerTypeGet, EmployerTypeDelete

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["employer_types"])


@router.get("/employer_type", status_code=status.HTTP_200_OK)
def fetch_employer_types() -> EmployerTypesResponse:
    employer_types = crud.employer_type.get_multi()
    return EmployerTypesResponse(employer_types=employer_types)


@router.get("/employer_type/search", status_code=status.HTTP_200_OK)
def search_employer_types(schema: EmployerTypeSearch = Depends()) -> EmployerTypesResponse:
    employer_types = crud.employer_type.search_by_name(employer_type_name=schema.employer_type_name, limit=schema.max_results)
    return EmployerTypesResponse(employer_types=employer_types)


@router.post("/employer_type", status_code=status.HTTP_201_CREATED)
def create_employer_type(employer_type_in: EmployerTypeCreate) -> EmployerTypeResponse:
    employer_type = crud.employer_type.create(obj_in=employer_type_in)
    return EmployerTypeResponse.from_orm(employer_type)


@router.put("/employer_type", status_code=status.HTTP_200_OK)
def update_employer_type(employer_type_in: EmployerTypeUpdate) -> EmployerTypeResponse:
    employer_type = crud.employer_type.get(id=employer_type_in.id)
    updated_employer_type = crud.employer_type.update(db_obj=employer_type, obj_in=employer_type_in)
    return EmployerTypeResponse.from_orm(updated_employer_type)


@router.get("/employer_type/{employer_type_id}", status_code=status.HTTP_200_OK)
def fetch_employer_type(schema: EmployerTypeGet = Depends()) -> EmployerTypeResponse:
    employer_type = crud.employer_type.get(id=schema.employer_type_id)
    return EmployerTypeResponse.from_orm(employer_type)


@router.delete("/employer_type/{employer_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employer_type(schema: EmployerTypeDelete = Depends()):
    crud.employer_type.delete(id=schema.employer_type_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
