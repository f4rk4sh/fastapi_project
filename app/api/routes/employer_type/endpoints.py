from typing import List, Optional

from fastapi import status
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.manager.manager_employer_type import employer_type
from app.schemas.employer_type import EmployerTypeCreate, EmployerTypeResponse, EmployerTypeUpdate
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Employer Types"])
descriptions = CRUDEndpointsDescriptions(model_name="Employer Type", search_parameters=["name"])
parameters = CRUDParamsDescriptions(obj_name="Employer Type")


@router.get("/employer_type", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
def fetch_employer_types() -> List[EmployerTypeResponse]:
    return employer_type.fetch_all()


@router.get("/employer_type/search", status_code=status.HTTP_200_OK, description=descriptions.search)
def search_employer_types(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
) -> List[EmployerTypeResponse]:
    return employer_type.search(parameter, keyword, max_results)


@router.post("/employer_type", status_code=status.HTTP_201_CREATED, description=descriptions.create)
def create_employer_type(employer_type_in: EmployerTypeCreate) -> EmployerTypeResponse:
    return employer_type.create(employer_type_in)


@router.put("/employer_type", status_code=status.HTTP_200_OK, description=descriptions.update)
def update_employer_type(employer_type_in: EmployerTypeUpdate) -> EmployerTypeResponse:
    return employer_type.update(employer_type_in)


@router.get("/employer_type/{employer_type_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
def fetch_employer_type(
    employer_type_id: PositiveInt = parameters.get_id,
) -> EmployerTypeResponse:
    return employer_type.fetch_one(employer_type_id)


@router.delete("/employer_type/{employer_type_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
def delete_employer_type(employer_type_id: PositiveInt = parameters.delete_id):
    return employer_type.delete(employer_type_id)
