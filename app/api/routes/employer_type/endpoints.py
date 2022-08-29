from typing import Optional

from fastapi_utils.inferring_router import InferringRouter
from fastapi import status, Response
from pydantic import PositiveInt

from app import crud
from app.api.routes.descriptions.employer_type_params_description import employer_type_params
from app.core.documentation.openapi_descriptions import CRUDDescriptions
from app.core.exceptions.exception_route_handler import ExceptionRouteHandler
from app.db.models import EmployerType
from app.schemas.employer_type import EmployerTypesResponse, EmployerTypeCreate, \
    EmployerTypeResponse, EmployerTypeUpdate

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Employer Types"])
descriptions = CRUDDescriptions(model=EmployerType, search_parameters=["name"])


@router.get("/employer_type", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
def fetch_employer_types() -> EmployerTypesResponse:
    employer_types = crud.employer_type.get_multi()
    return EmployerTypesResponse(employer_types=employer_types)


@router.get("/employer_type/search", status_code=status.HTTP_200_OK, description=descriptions.search)
def search_employer_types(
        parameter: str = employer_type_params.search_parameter,
        keyword: str = employer_type_params.search_keyword,
        max_results: Optional[PositiveInt] = employer_type_params.max_results_search
) -> EmployerTypesResponse:
    employer_types = crud.employer_type.search_by_parameter(parameter=parameter, keyword=keyword, limit=max_results)
    return EmployerTypesResponse(employer_types=employer_types)


@router.post("/employer_type", status_code=status.HTTP_201_CREATED, description=descriptions.create)
def create_employer_type(employer_type_in: EmployerTypeCreate) -> EmployerTypeResponse:
    employer_type = crud.employer_type.create(obj_in=employer_type_in)
    return EmployerTypeResponse.from_orm(employer_type)


@router.put("/employer_type", status_code=status.HTTP_200_OK, description=descriptions.update)
def update_employer_type(employer_type_in: EmployerTypeUpdate) -> EmployerTypeResponse:
    employer_type = crud.employer_type.get(id=employer_type_in.id)
    updated_employer_type = crud.employer_type.update(db_obj=employer_type, obj_in=employer_type_in)
    return EmployerTypeResponse.from_orm(updated_employer_type)


@router.get("/employer_type/{employer_type_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
def fetch_employer_type(employer_type_id: PositiveInt = employer_type_params.get_id) -> EmployerTypeResponse:
    employer_type = crud.employer_type.get(id=employer_type_id)
    return EmployerTypeResponse.from_orm(employer_type)


@router.delete("/employer_type/{employer_type_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
def delete_employer_type(employer_type_id: PositiveInt = employer_type_params.delete_id):
    crud.employer_type.delete(id=employer_type_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
