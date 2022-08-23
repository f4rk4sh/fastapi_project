from fastapi_utils.inferring_router import InferringRouter
from fastapi import status, Depends, Response

from app import crud
from app.core.exceptions.exception_route_handler import ExceptionRouteHandler
from app.schemas.employer import EmployersResponse, EmployerSearchResponse, EmployerSearch, EmployerCreate, \
    EmployerResponse, EmployerUpdate, EmployerGet, EmployerDelete

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["employers"])


@router.get("/employer", status_code=status.HTTP_200_OK)
def fetch_employers() -> EmployersResponse:
    employers = crud.employer.get_multi()
    results = [EmployerResponse(**{**employer.user.__dict__, **employer.__dict__}) for employer in employers]
    return EmployersResponse(employers=results)


@router.get("/employer/search", status_code=status.HTTP_200_OK)
def search_employers(schema: EmployerSearch = Depends()) -> EmployerSearchResponse:
    employers = crud.employer.search_by_name(employer_name=schema.employer_name, limit=schema.max_results)
    results = [EmployerResponse(**{**employer.user.__dict__, **employer.__dict__}) for employer in employers]
    return EmployerSearchResponse(results=results)


@router.post("/employer", status_code=status.HTTP_201_CREATED)
def create_employer(employer_in: EmployerCreate) -> EmployerResponse:
    employer = crud.employer.create(obj_in=employer_in)
    return EmployerResponse(**{**employer.user.__dict__, **employer.__dict__})


@router.put("/employer", status_code=status.HTTP_200_OK)
def update_employer(employer_in: EmployerUpdate) -> EmployerResponse:
    employer = crud.employer.get(id=employer_in.id)
    updated_employer = crud.employer.update(db_obj=employer, obj_in=employer_in)
    return EmployerResponse(**{**updated_employer.user.__dict__, **updated_employer.__dict__})


@router.get("/employer/{employer_id}", status_code=status.HTTP_200_OK)
def fetch_employer(schema: EmployerGet = Depends()) -> EmployerResponse:
    employer = crud.employer.get(id=schema.employer_id)
    return EmployerResponse(**{**employer.user.__dict__, **employer.__dict__})


@router.delete("/employer/{employer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_employer(schema: EmployerDelete = Depends()):
    crud.employer.delete(id=schema.employer_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
