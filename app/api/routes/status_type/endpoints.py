from typing import List, Optional

from fastapi import status
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.manager.manager_status_type import status_type
from app.schemas.status_type import StatusTypeCreate, StatusTypeResponse, StatusTypeUpdate
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Status Types"])
descriptions = CRUDEndpointsDescriptions(model_name="Status Type", search_parameters=["name"])
parameters = CRUDParamsDescriptions(obj_name="Status Type")


@router.get("/status_type", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
def fetch_status_types() -> List[StatusTypeResponse]:
    return status_type.fetch_all()


@router.get("/status_type/search", status_code=status.HTTP_200_OK, description=descriptions.search)
def search_status_types(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
) -> List[StatusTypeResponse]:
    return status_type.search(parameter, keyword, max_results)


@router.post("/status_type", status_code=status.HTTP_201_CREATED, description=descriptions.create)
def create_status_type(status_type_in: StatusTypeCreate) -> StatusTypeResponse:
    return status_type.create(status_type_in)


@router.put("/status_type", status_code=status.HTTP_200_OK, description=descriptions.update)
def update_status_type(status_type_in: StatusTypeUpdate) -> StatusTypeResponse:
    return status_type.update(status_type_in)


@router.get("/status_type/{status_type_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
def fetch_status_type(
    status_type_id: PositiveInt = parameters.get_id,
) -> StatusTypeResponse:
    return status_type.fetch_one(status_type_id)


@router.delete("/status_type/{status_type_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
def delete_status_type(status_type_id: PositiveInt = parameters.delete_id):
    return status_type.delete(status_type_id)
