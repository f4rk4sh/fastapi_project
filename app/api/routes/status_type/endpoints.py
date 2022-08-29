from typing import Optional

from fastapi_utils.inferring_router import InferringRouter
from fastapi import status, Response
from pydantic import PositiveInt

from app import crud
from app.api.routes.descriptions.status_type_params_description import status_type_params
from app.core.documentation.openapi_descriptions import CRUDDescriptions
from app.core.exceptions.exception_route_handler import ExceptionRouteHandler
from app.db.models import StatusType
from app.schemas.status_type import StatusTypesResponse, StatusTypeSearchResults, StatusTypeUpdate, \
    StatusTypeResponse, StatusTypeCreate

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Status Types"])
descriptions = CRUDDescriptions(model=StatusType, search_parameters=["name"])


@router.get("/status_type", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
def fetch_status_types() -> StatusTypesResponse:
    status_types = crud.status_type.get_multi()
    return StatusTypesResponse(status_types=status_types)


@router.get("/status_type/search", status_code=status.HTTP_200_OK, description=descriptions.search)
def search_status_types(
        parameter: str = status_type_params.search_parameter,
        keyword: str = status_type_params.search_keyword,
        max_results: Optional[PositiveInt] = status_type_params.max_results_search
) -> StatusTypeSearchResults:
    results = crud.status_type.search_by_parameter(parameter=parameter, keyword=keyword, limit=max_results)
    return StatusTypeSearchResults(results=results)


@router.post("/status_type", status_code=status.HTTP_201_CREATED, description=descriptions.create)
def create_status_type(status_type_in: StatusTypeCreate) -> StatusTypeResponse:
    status_type = crud.status_type.create(obj_in=status_type_in)
    return StatusTypeResponse.from_orm(status_type)


@router.put("/status_type", status_code=status.HTTP_200_OK, description=descriptions.update)
def update_status_type(status_type_in: StatusTypeUpdate) -> StatusTypeResponse:
    status_type = crud.status_type.get(id=status_type_in.id)
    updated_status_type = crud.status_type.update(db_obj=status_type, obj_in=status_type_in)
    return StatusTypeResponse.from_orm(updated_status_type)


@router.get("/status_type/{status_type_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
def fetch_status_type(status_type_id: PositiveInt = status_type_params.get_id) -> StatusTypeResponse:
    status_type = crud.status_type.get(id=status_type_id)
    return StatusTypeResponse.from_orm(status_type)


@router.delete("/status_type/{status_type_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
def delete_status_type(status_type_id: PositiveInt = status_type_params.delete_id):
    crud.status_type.delete(id=status_type_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
