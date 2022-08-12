from typing import Optional

from fastapi import status, Query
from fastapi.responses import Response
from fastapi_utils.inferring_router import InferringRouter

from app import crud
from app.core.exceptions.exception_route_handler import ExceptionRouteHandler
from app.schemas.role import RoleResponse, RolesResponse, RoleSearchResults, RoleCreate, RoleUpdate

router = InferringRouter(route_class=ExceptionRouteHandler, tags=["roles"])


@router.get("/role", status_code=status.HTTP_200_OK)
def fetch_roles() -> RolesResponse:
    """
    Fetch all roles from the database
    """
    roles = crud.role.get_multi()
    return RolesResponse(roles=roles)


@router.get("/role/search", status_code=status.HTTP_200_OK)
def search_roles(
    role_name: str = Query(min_length=3),
    max_results: Optional[int] = Query(None, gt=0),
) -> RoleSearchResults:
    """
    Search for roles in the database based on name keyword
    """
    results = crud.role.search_by_name(role_name=role_name, limit=max_results)
    return RoleSearchResults(results=results)


@router.post("/role", status_code=status.HTTP_201_CREATED)
def create_role(role_in: RoleCreate) -> RoleResponse:
    """
    Create a new role in the database
    """
    role = crud.role.create(obj_in=role_in)
    return RoleResponse.from_orm(role)


@router.put("/role", status_code=status.HTTP_200_OK)
def update_role(recipe_in: RoleUpdate) -> RoleResponse:
    """
    Update role in the database
    """
    role = crud.role.get(id=recipe_in.id)
    updated_role = crud.role.update(db_obj=role, obj_in=recipe_in)
    return RoleResponse.from_orm(updated_role)


@router.get("/role/{role_id}", status_code=status.HTTP_200_OK)
def fetch_role(role_id: int) -> RoleResponse:
    """
    Fetch a single role from the database by ID
    """
    role = crud.role.get(id=role_id)
    return RoleResponse.from_orm(role)


@router.delete("/role/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int):
    """
    Delete role from the database
    """
    crud.role.delete(id=role_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
