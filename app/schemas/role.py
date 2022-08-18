from typing import List, Optional

from fastapi import Path, Query
from pydantic import BaseModel, Field, PositiveInt, validator

from app import crud
from app.core.exceptions.common_exceptions import HTTPBadRequestException


class RoleBase(BaseModel):
    name: str = Field(
        ...,
        title="The NAME of the role",
        description="Note: must be a string with a length of less than 50 characters",
        example="admin",
        max_length=50
    )


class RoleCreate(RoleBase):
    @validator("name")
    def unique_name(cls, role_name: str) -> str:
        role = crud.role.get_by_name(role_name)
        if role:
            raise HTTPBadRequestException(detail="Role with this name already exists")
        return role_name


class RoleUpdate(RoleBase):
    id: PositiveInt = Field(
        ...,
        title="The ID of the role",
        description="Note: must be a positive integer",
        example=1
    )


class RoleResponse(RoleBase):
    id: PositiveInt = Field(
        ...,
        title="The ID of the role",
        description="Note: must be a positive integer",
        example=1
    )

    class Config:
        orm_mode = True


class RolesResponse(BaseModel):
    roles: List[RoleResponse] = Field(
        title="The list of the roles",
        alias="roles",
    )


class RoleSearchResults(BaseModel):
    results: List[RoleResponse] = Field(
        title="The list of the roles matching search parameters",
        alias="results",
    )


class RoleGet:
    def __init__(self,
                 role_id: PositiveInt = Path(
                     description="The ID of the role to fetch\n\n"
                                 "**Note:** must be a positive integer")
                 ):
        self.role_id = role_id


class RoleDelete:
    def __init__(self,
                 role_id: PositiveInt = Path(
                     description="The ID of the role to delete\n\n"
                                 "**Note:** must be a positive integer")
                 ):
        self.role_id = role_id


class RoleSearch:
    def __init__(self,
                 role_name: str = Query(
                     ...,
                     description="The NAME of the role to search\n\n"
                                 "**Note:** must be a string with a length of more than 3 characters",
                     min_length=3
                 ),
                 max_results: Optional[PositiveInt] = Query(
                     None,
                     description="The total amount of the roles matching search parameters to fetch\n\n"
                                 "**Note:** must be a positive integer",
                 )):
        self.role_name = role_name
        self.max_results = max_results
