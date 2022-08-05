from typing import Any, Optional

from fastapi import APIRouter, status, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import crud
from app.db.get_database import get_db
from app.schemas.role import RoleResponse, RolesResponse, RoleSearchResults, RoleCreate, RoleUpdate

router = APIRouter()


@router.get("/{role_id}", status_code=status.HTTP_200_OK, response_model=RoleResponse)
def fetch_role(*, role_id: int, db: Session = Depends(get_db)) -> Any:
    """
    Fetch a single role from the database by ID
    """
    role = crud.role.get(db=db, id=role_id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with ID {role_id} not found")
    return role


@router.get("/all/", status_code=status.HTTP_200_OK, response_model=RolesResponse)
def fetch_roles(*, db: Session = Depends(get_db)):
    """
    Fetch all roles from the database
    """
    roles = crud.role.get_multi(db=db)
    if not roles:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Roles not found")
    return {"roles": roles}


@router.get("/search/", status_code=status.HTTP_200_OK, response_model=RoleSearchResults)
def search_roles(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="admin"),
    max_results: Optional[int] = Query(None, gt=0, example=10),
    db: Session = Depends(get_db),
) -> dict:
    """
    Search for roles in the database based on name keyword
    """
    roles = crud.role.get_multi(db=db, limit=max_results)
    if not keyword:
        return {"results": roles}

    results = filter(lambda recipe: keyword.lower() in recipe.name.lower(), roles)
    return {"results": list(results)[:max_results]}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RoleResponse)
def create_role(*, role_in: RoleCreate, db: Session = Depends(get_db)):
    """
    Create a new role in the database
    """
    role = crud.role.create(db=db, obj_in=role_in)
    return role


@router.put("/", status_code=status.HTTP_201_CREATED, response_model=RoleResponse)
def update_role(*, recipe_in: RoleUpdate, db: Session = Depends(get_db)):
    """
    Update role in the database
    """
    role = crud.role.get(db=db, id=recipe_in.id)
    if not role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Role with ID {recipe_in.id} not found")
    updated_role = crud.role.update(db=db, db_obj=role, obj_in=recipe_in)
    return updated_role


@router.delete("/{role_id}", status_code=status.HTTP_200_OK, response_model=RoleResponse)
def delete_role(*, role_id: int, db: Session = Depends(get_db)):
    """
    Delete role from the database
    """
    # ToDo ?checking the existence of the role requested for deletion
    role = crud.role.delete(db=db, id=role_id)
    return role


