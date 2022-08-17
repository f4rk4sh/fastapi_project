from fastapi import status, Depends
from fastapi.responses import Response
from fastapi_utils.inferring_router import InferringRouter

from app import crud
from app.core.documentation.openapi_descriptions import get_crud_descriptions
from app.core.exceptions.exception_route_handler import ExceptionRouteHandler
from app.core.documentation.openapi_tags import get_crud_tag_name
from app.db.models import Role
from app.schemas.role import RoleResponse, RolesResponse, RoleSearchResults, RoleCreate, RoleUpdate, RoleGet, \
    RoleDelete, RoleSearch

router = InferringRouter(route_class=ExceptionRouteHandler, tags=[get_crud_tag_name(Role)])
descriptions = get_crud_descriptions(model=Role, search_keywords=["name"])


@router.get("/role", status_code=status.HTTP_200_OK, description=descriptions["fetch_all"])
def fetch_roles() -> RolesResponse:
    roles = crud.role.get_multi()
    return RolesResponse(roles=roles)


@router.get("/role/search", status_code=status.HTTP_200_OK, description=descriptions["search"])
def search_roles(schema: RoleSearch = Depends()) -> RoleSearchResults:
    results = crud.role.search_by_name(role_name=schema.role_name, limit=schema.max_results)
    return RoleSearchResults(results=results)


@router.post("/role", status_code=status.HTTP_201_CREATED, description=descriptions["create"])
def create_role(role_in: RoleCreate) -> RoleResponse:
    role = crud.role.create(obj_in=role_in)
    return RoleResponse.from_orm(role)


@router.put("/role", status_code=status.HTTP_200_OK, description=descriptions["update"])
def update_role(recipe_in: RoleUpdate) -> RoleResponse:
    role = crud.role.get(id=recipe_in.id)
    updated_role = crud.role.update(db_obj=role, obj_in=recipe_in)
    return RoleResponse.from_orm(updated_role)


@router.get("/role/{role_id}", status_code=status.HTTP_200_OK, description=descriptions["fetch_one"])
def fetch_role(schema: RoleGet = Depends()) -> RoleResponse:
    role = crud.role.get(id=schema.role_id)
    return RoleResponse.from_orm(role)


@router.delete("/role/{role_id}", status_code=status.HTTP_204_NO_CONTENT, description=descriptions["delete"])
def delete_role(schema: RoleDelete = Depends()):
    crud.role.delete(id=schema.role_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
