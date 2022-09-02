from typing import Optional, List

from fastapi_utils.inferring_router import InferringRouter
from fastapi import status
from pydantic import PositiveInt

from app.api.routes.descriptions.employer_params_description import employer_params
from app.core.documentation.openapi_descriptions import CRUDDescriptions
from app.core.exceptions.exception_route_handler import ExceptionRouteHandler
from app.db.models import Employer
from app.manager.employer import employer_manager
from app.schemas.employer import EmployerCreate, EmployerResponse, EmployerUpdate

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Employers"])
descriptions = CRUDDescriptions(model=Employer, search_parameters=["email", "phone", "name", "address", "edrpou"])


@router.get("/employer", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
def fetch_employers() -> List[EmployerResponse]:
    return employer_manager.fetch_all()


@router.get("/employer/search", status_code=status.HTTP_200_OK, description=descriptions.search)
def search_employers(
        parameter: str = employer_params.search_parameter,
        keyword: str = employer_params.search_keyword,
        max_results: Optional[PositiveInt] = employer_params.max_results_search
) -> List[EmployerResponse]:
    return employer_manager.search(parameter, keyword, max_results)


@router.post("/employer", status_code=status.HTTP_201_CREATED, description=descriptions.create)
def create_employer(employer_in: EmployerCreate) -> EmployerResponse:
    return employer_manager.create(employer_in)


@router.put("/employer", status_code=status.HTTP_200_OK, description=descriptions.update)
def update_employer(employer_in: EmployerUpdate) -> EmployerResponse:
    return employer_manager.update(employer_in)


@router.get("/employer/{employer_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
def fetch_employer(employer_id: PositiveInt = employer_params.get_id) -> EmployerResponse:
    return employer_manager.fetch_one(employer_id)


@router.delete("/employer/{employer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employer(employer_id: PositiveInt = employer_params.delete_id):
    return employer_manager.delete(employer_id)
