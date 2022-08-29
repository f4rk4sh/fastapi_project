from typing import List

from pydantic import BaseModel, Field, PositiveInt, validator

from app import crud
from app.core.exceptions.common_exceptions import HTTPBadRequestException


class StatusTypeBase(BaseModel):
    name: str = Field(
        title="The NAME of the status type",
        description="Note: must be a string with a length of less than 50 characters",
        example="not active",
        max_length=50
    )


class StatusTypeCreate(StatusTypeBase):
    @validator("name")
    def unique_name(cls, value: str) -> str:
        status_type = crud.status_type.get_by_attribute(attribute="name", value=value)
        if status_type:
            raise HTTPBadRequestException(detail="Status type with this name already exists")
        return value


class StatusTypeUpdate(StatusTypeBase):
    id: PositiveInt = Field(
        title="The ID of the status type",
        description="Note: must be a positive integer",
        example=1
    )


class StatusTypeResponse(StatusTypeBase):
    id: PositiveInt = Field(
        title="The ID of the status type",
        description="Note: must be a positive integer",
        example=1
    )

    class Config:
        orm_mode = True


class StatusTypesResponse(BaseModel):
    status_types: List[StatusTypeResponse] = Field(
        title="The list of the status types",
        alias="status_types",
    )


class StatusTypeSearchResults(BaseModel):
    results: List[StatusTypeResponse] = Field(
        title="The list of the status types matching search parameters",
        alias="results",
    )
