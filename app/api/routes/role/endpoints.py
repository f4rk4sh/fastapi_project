from typing import Optional

from fastapi import status
from fastapi.responses import Response
from fastapi_utils.inferring_router import InferringRouter
from pydantic import PositiveInt

from app import crud
from app.api.routes.descriptions.role_params_description import role_params
from app.core.documentation.openapi_descriptions import CRUDDescriptions
from app.core.exceptions.exception_route_handler import ExceptionRouteHandler
from app.db.models import Role
from app.schemas.role import RoleResponse, RolesResponse, RoleSearchResults, RoleCreate, RoleUpdate

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["Roles"])
descriptions = CRUDDescriptions(model=Role, search_parameters=["name"])


@router.get("/role", status_code=status.HTTP_200_OK, description=descriptions.fetch_all)
def fetch_roles() -> RolesResponse:
    roles = crud.role.get_multi()
    return RolesResponse(roles=roles)


@router.get("/role/search", status_code=status.HTTP_200_OK, description=descriptions.search)
def search_roles(
        parameter: str = role_params.search_parameter,
        keyword: str = role_params.search_keyword,
        max_results: Optional[PositiveInt] = role_params.max_results_search
) -> RoleSearchResults:
    results = crud.role.search_by_parameter(parameter=parameter, keyword=keyword, limit=max_results)
    return RoleSearchResults(results=results)


@router.post("/role", status_code=status.HTTP_201_CREATED, description=descriptions.create)
def create_role(role_in: RoleCreate) -> RoleResponse:
    role = crud.role.create(obj_in=role_in)
    return RoleResponse.from_orm(role)


@router.put("/role", status_code=status.HTTP_200_OK, description=descriptions.update)
def update_role(recipe_in: RoleUpdate) -> RoleResponse:
    role = crud.role.get(id=recipe_in.id)
    updated_role = crud.role.update(db_obj=role, obj_in=recipe_in)
    return RoleResponse.from_orm(updated_role)


@router.get("/role/{role_id}", status_code=status.HTTP_200_OK, description=descriptions.fetch_one)
def fetch_role(role_id: PositiveInt = role_params.get_id) -> RoleResponse:
    role = crud.role.get(id=role_id)
    return RoleResponse.from_orm(role)


@router.delete("/role/{role_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions.delete)
def delete_role(role_id: PositiveInt = role_params.delete_id):
    crud.role.delete(id=role_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
