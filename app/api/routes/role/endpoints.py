from typing import List, Optional

from fastapi import status
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app.api.docs.api_endpoints import CRUDEndpointsDescriptions
from app.api.docs.api_params import CRUDParamsDescriptions
from app.manager.manager_role import role
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.utils.exceptions.exception_route_handler import ExceptionRouteHandler

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Roles"])
descriptions = CRUDEndpointsDescriptions(model_name="Role", search_parameters=["name"])
parameters = CRUDParamsDescriptions(obj_name="Role")


@router.get("/role", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
def fetch_roles() -> List[RoleResponse]:
    return role.fetch_all()


@router.get("/role/search", status_code=status.HTTP_200_OK, description=descriptions.search)
def search_roles(
    parameter: str = parameters.search_parameter,
    keyword: str = parameters.search_keyword,
    max_results: Optional[PositiveInt] = parameters.max_results_search,
) -> List[RoleResponse]:
    return role.search(parameter, keyword, max_results)


@router.post("/role", status_code=status.HTTP_201_CREATED, description=descriptions.create)
def create_role(role_in: RoleCreate) -> RoleResponse:
    return role.create(role_in)


@router.put("/role", status_code=status.HTTP_200_OK, description=descriptions.update)
def update_role(recipe_in: RoleUpdate) -> RoleResponse:
    return role.update(recipe_in)


@router.get("/role/{role_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
def fetch_role(role_id: PositiveInt = parameters.get_id) -> RoleResponse:
    return role.fetch_one(role_id)


@router.delete("/role/{role_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
def delete_role(role_id: PositiveInt = parameters.delete_id):
    return role.delete(role_id)
