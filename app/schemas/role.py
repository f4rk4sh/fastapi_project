from typing import List

from pydantic import BaseModel, Field, PositiveInt, validator

from app import crud
from app.core.exceptions.common_exceptions import HTTPBadRequestException


class RoleBase(BaseModel):
    name: str = Field(
        title="The NAME of the role",
        description="Note: must be a string with a length of less than 50 characters",
        example="admin",
        max_length=50
    )


class RoleCreate(RoleBase):
    @validator("name")
    def unique_name(cls, value: str) -> str:
        role = crud.role.get_by_attribute(attribute="name", value=value)
        if role:
            raise HTTPBadRequestException(detail="Role with this name already exists")
        return value


class RoleUpdate(RoleBase):
    id: PositiveInt = Field(
        title="The ID of the role",
        description="Note: must be a positive integer",
        example=1
    )


class RoleResponse(RoleBase):
    id: PositiveInt = Field(
        title="The ID of the role",
        description="Note: must be a positive integer",
        example=1
    )

    class Config:
        orm_mode = True


class RolesResponse(BaseModel):
    roles: List[RoleResponse] = Field(
        title="The list of the roles"
    )


class RoleSearchResults(BaseModel):
    results: List[RoleResponse] = Field(
        title="The list of the roles matching search parameters"
    )
