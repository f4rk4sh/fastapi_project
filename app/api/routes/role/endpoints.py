from typing import Optional

from fastapi import status, HTTPException, Query
from fastapi.responses import Response
from fastapi_utils.inferring_router import InferringRouter

from app import crud
from app.schemas.role import RoleResponse, RolesResponse, RoleSearchResults, RoleCreate, RoleUpdate

router = InferringRouter(tags=["roles"])


@router.get("/role", status_code=status.HTTP_200_OK)
def fetch_roles() -> RolesResponse:
    """
    Fetch all roles from the database
    """
    roles = crud.role.get_multi()
    if not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roles not found")
    return RolesResponse(roles=roles)


@router.get("/role/search", status_code=status.HTTP_200_OK)
def search_roles(
    role_name: Optional[str] = Query(None, min_length=3, example="admin"),
    max_results: Optional[int] = Query(None, gt=0),
) -> RoleSearchResults:
    """
    Search for roles in the database based on name keyword
    """
    results = crud.role.search_by_name(role_name=role_name, limit=max_results)
    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No results found")
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
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with ID {recipe_in.id} not found")
    updated_role = crud.role.update(db_obj=role, obj_in=recipe_in)
    return RoleResponse.from_orm(updated_role)


@router.get("/role/{role_id}", status_code=status.HTTP_200_OK)
def fetch_role(role_id: int) -> RoleResponse:
    """
    Fetch a single role from the database by ID
    """
    role = crud.role.get(id=role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with ID {role_id} not found")
    return RoleResponse.from_orm(role)


@router.delete("/role/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int):
    """
    Delete role from the database
    """
    role = crud.role.get(id=role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with ID {role_id} not found")
    crud.role.delete(id=role_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
