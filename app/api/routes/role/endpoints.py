from typing import Any, Optional

from fastapi import APIRouter, status, HTTPException, Query

from app import crud
from app.schemas.role import RoleResponse, RolesResponse, RoleSearchResults, RoleCreate, RoleUpdate

router = APIRouter(tags=["roles"])


@router.get("/role/{role_id}", status_code=status.HTTP_200_OK, response_model=RoleResponse)
def fetch_role(*, role_id: int) -> Any:
    """
    Fetch a single role from the database by ID
    """
    role = crud.role.get(id=role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with ID {role_id} not found")
    return RoleResponse.from_orm(role)


@router.get("/role/all/", status_code=status.HTTP_200_OK, response_model=RolesResponse)
def fetch_roles():
    """
    Fetch all roles from the database
    """
    roles = crud.role.get_multi()
    if not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roles not found")
    return RolesResponse(roles=roles)


@router.get("/role/search/", status_code=status.HTTP_200_OK, response_model=RoleSearchResults)
def search_roles(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="admin"),
    max_results: Optional[int] = Query(None, gt=0, example=10),
):
    """
    Search for roles in the database based on name keyword
    """
    roles = crud.role.get_multi(limit=max_results)
    if not keyword:
        return RoleSearchResults(results=roles)
    results = list(filter(lambda role: keyword.lower() in role.name.lower(), roles))[:max_results]
    return RoleSearchResults(results=results)


@router.post("/role/add/", status_code=status.HTTP_201_CREATED, response_model=RoleResponse)
def create_role(*, role_in: RoleCreate):
    """
    Create a new role in the database
    """
    role = crud.role.create(obj_in=role_in)
    return RoleResponse.from_orm(role)


@router.put("/role/update/", status_code=status.HTTP_201_CREATED, response_model=RoleResponse)
def update_role(*, recipe_in: RoleUpdate):
    """
    Update role in the database
    """
    role = crud.role.get(id=recipe_in.id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with ID {recipe_in.id} not found")
    updated_role = crud.role.update(db_obj=role, obj_in=recipe_in)
    return RoleResponse.from_orm(updated_role)


@router.delete("/role/{role_id}/delete/", status_code=status.HTTP_200_OK, response_model=RoleResponse)
def delete_role(*, role_id: int):
    """
    Delete role from the database
    """
    # ToDo ?checking the existence of the role requested for deletion
    role = crud.role.delete(id=role_id)
    return RoleResponse.from_orm(role)


