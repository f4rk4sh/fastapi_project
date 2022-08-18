from fastapi_utils.inferring_router import InferringRouter
from fastapi import status, Depends, Response

from app import crud
from app.core.exceptions.exception_route_handler import ExceptionRouteHandler
from app.schemas.status_type import StatusTypesResponse, StatusTypeSearchResults, StatusTypeSearch, StatusTypeUpdate, \
    StatusTypeResponse, StatusTypeCreate, StatusTypeGet, StatusTypeDelete

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["status_types"])


@router.get("/status_type", status_code=status.HTTP_200_OK)
def fetch_status_types() -> StatusTypesResponse:
    status_types = crud.status_type.get_multi()
    return StatusTypesResponse(status_types=status_types)


@router.get("/status_type/search", status_code=status.HTTP_200_OK)
def search_status_types(schema: StatusTypeSearch = Depends()) -> StatusTypeSearchResults:
    results = crud.status_type.search_by_name(status_type_name=schema.status_type_name, limit=schema.max_results)
    return StatusTypeSearchResults(results=results)


@router.post("/status_type", status_code=status.HTTP_201_CREATED)
def create_status_type(status_type_in: StatusTypeCreate) -> StatusTypeResponse:
    status_type = crud.status_type.create(obj_in=status_type_in)
    return StatusTypeResponse.from_orm(status_type)


@router.put("/status_type", status_code=status.HTTP_200_OK)
def update_status_type(status_type_in: StatusTypeUpdate) -> StatusTypeResponse:
    status_type = crud.status_type.get(id=status_type_in.id)
    updated_status_type = crud.status_type.update(db_obj=status_type, obj_in=status_type_in)
    return StatusTypeResponse.from_orm(updated_status_type)


@router.get("/status_type/{status_type_id}", status_code=status.HTTP_200_OK)
def fetch_status_type(schema: StatusTypeGet = Depends()) -> StatusTypeResponse:
    status_type = crud.status_type.get(id=schema.status_type_id)
    return StatusTypeResponse.from_orm(status_type)


@router.delete("/status_type/{status_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_status_type(schema: StatusTypeDelete = Depends()):
    crud.status_type.delete(id=schema.status_type_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
