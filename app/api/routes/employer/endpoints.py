from typing import Optional

from fastapi_utils.inferring_router import InferringRouter
from fastapi import status, Response
from pydantic import PositiveInt

from app import crud
from app.api.routes.descriptions.employer_params_description import employer_params
from app.core.documentation.openapi_descriptions import CRUDDescriptions
from app.core.exceptions.exception_route_handler import ExceptionRouteHandler
from app.db.models import Employer
from app.schemas.employer import EmployersResponse, EmployerSearchResponse, EmployerCreate, \
    EmployerResponse, EmployerUpdate

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Employers"])
descriptions = CRUDDescriptions(model=Employer, search_parameters=["name", "address", "edrpou"])


@router.get("/employer", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
def fetch_employers() -> EmployersResponse:
    employers = crud.employer.get_multi()
    results = [EmployerResponse(**{**employer.user.__dict__, **employer.__dict__}) for employer in employers]
    return EmployersResponse(employers=results)


@router.get("/employer/search", status_code=status.HTTP_200_OK, description=descriptions.search)
def search_employers(
        parameter: str = employer_params.search_parameter,
        keyword: str = employer_params.search_keyword,
        max_results: Optional[PositiveInt] = employer_params.max_results_search
) -> EmployerSearchResponse:
    employers = crud.employer.search_by_parameter(parameter=parameter, keyword=keyword, limit=max_results)
    results = [EmployerResponse(**{**employer.user.__dict__, **employer.__dict__}) for employer in employers]
    return EmployerSearchResponse(results=results)


@router.post("/employer", status_code=status.HTTP_201_CREATED, description=descriptions.create)
def create_employer(employer_in: EmployerCreate) -> EmployerResponse:
    employer = crud.employer.create(obj_in=employer_in)
    return EmployerResponse(**{**employer.user.__dict__, **employer.__dict__})


@router.put("/employer", status_code=status.HTTP_200_OK, description=descriptions.update)
def update_employer(employer_in: EmployerUpdate) -> EmployerResponse:
    employer = crud.employer.get(id=employer_in.id)
    updated_employer = crud.employer.update(db_obj=employer, obj_in=employer_in)
    return EmployerResponse(**{**updated_employer.user.__dict__, **updated_employer.__dict__})


@router.get("/employer/{employer_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
def fetch_employer(employer_id: PositiveInt = employer_params.get_id) -> EmployerResponse:
    employer = crud.employer.get(id=employer_id)
    return EmployerResponse(**{**employer.user.__dict__, **employer.__dict__})


@router.delete("/employer/{employer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employer(employer_id: PositiveInt = employer_params.delete_id):
    crud.employer.delete(id=employer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
