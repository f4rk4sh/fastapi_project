from typing import List, Optional

from fastapi import status
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.manager.manager_employer import employer
from app.schemas.employer import EmployerCreate, EmployerResponse, EmployerUpdate
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Employers"])
descriptions = CRUDEndpointsDescriptions(
    model_name="Employer",
    search_parameters=["email", "phone", "name", "address", "edrpou"]
)
parameters = CRUDParamsDescriptions(obj_name="Employer")


@router.get("/employer", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
def fetch_employers() -> List[EmployerResponse]:
    return employer.fetch_all()


@router.get("/employer/search", status_code=status.HTTP_200_OK, description=descriptions.search)
def search_employers(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
) -> List[EmployerResponse]:
    return employer.search(parameter, keyword, max_results)


@router.post("/employer", status_code=status.HTTP_201_CREATED, description=descriptions.create)
def create_employer(employer_in: EmployerCreate) -> EmployerResponse:
    return employer.create(employer_in)


@router.put("/employer", status_code=status.HTTP_200_OK, description=descriptions.update)
def update_employer(employer_in: EmployerUpdate) -> EmployerResponse:
    return employer.update(employer_in)


@router.get("/employer/{employer_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
def fetch_employer(employer_id: PositiveInt = parameters.get_id) -> EmployerResponse:
    return employer.fetch_one(employer_id)


@router.delete("/employer/{employer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employer(employer_id: PositiveInt = parameters.delete_id):
    return employer.delete(employer_id)
