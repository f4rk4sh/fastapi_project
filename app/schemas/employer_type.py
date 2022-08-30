from typing import List

from pydantic import BaseModel, Field, PositiveInt, validator

from app import crud
from app.core.exceptions.common_exceptions import HTTPBadRequestException


class EmployerTypeBase(BaseModel):
    name: str = Field(
        title="The NAME of the employer type",
        description="Note: must be a string with a length of less than 50 characters",
        example="AT",
        max_length=50
    )


class EmployerTypeCreate(EmployerTypeBase):
    @validator("name")
    def unique_name(cls, value: str) -> str:
        employer_type = crud.employer_type.get_by_attribute(attributes=["name"], value=value)
        if employer_type:
            raise HTTPBadRequestException(detail="Employer type with this name already exists")
        return value


class EmployerTypeUpdate(EmployerTypeBase):
    id: PositiveInt = Field(
        title="The ID of the employer type",
        description="Note: must be a positive integer",
        example=1
    )


class EmployerTypeResponse(EmployerTypeBase):
    id: PositiveInt = Field(
        title="The ID of the employer type",
        description="Note: must be a positive integer",
        example=1
    )

    class Config:
        orm_mode = True


class EmployerTypesResponse(BaseModel):
    employer_types: List[EmployerTypeResponse] = Field(
        title="The list of the employer types",
        alias="employer_types"
    )


class EmployerTypeSearchResults(BaseModel):
    results: List[EmployerTypeResponse] = Field(
        title="The list of the roles matching search parameters",
        alias="results",
    )
