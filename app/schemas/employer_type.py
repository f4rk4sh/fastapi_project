from typing import List, Optional

from fastapi import Path, Query
from pydantic import BaseModel, Field, PositiveInt, validator

from app import crud


class EmployerTypeBase(BaseModel):
    name: str = Field(
        ...,
        title="The NAME of the employer type",
        description="Note: must be a string with a length of less than 50 characters",
        example="AT",
        max_length=50
    )


class EmployerTypeCreate(EmployerTypeBase):
    # @validator("name")
    # def unique_name(cls, employer_type_name: str) -> str:
    #     employer_type = crud.employer_type.get_by_name(employer_type_name)
    #     if employer_type:
    #         raise HTTPBadRequestException(detail="Employer type with this name already exists")
    #     return employer_type_name
    pass


class EmployerTypeUpdate(EmployerTypeBase):
    id: PositiveInt = Field(
        ...,
        title="The ID of the employer type",
        description="Note: must be a positive integer",
        example=1
    )


class EmployerTypeResponse(EmployerTypeBase):
    id: PositiveInt = Field(
        ...,
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


class EmployerTypeGet:
    def __init__(self,
                 employer_type_id: PositiveInt = Path(
                     description="The ID of the employer type to fetch\n\n"
                                 "**Note:** must be a positive integer")
                 ):
        self.employer_type_id = employer_type_id


class EmployerTypeDelete:
    def __init__(self,
                 employer_type_id: PositiveInt = Path(
                     description="The ID of the employer type to delete\n\n"
                                 "**Note:** must be a positive integer")
                 ):
        self.employer_type_id = employer_type_id


class EmployerTypeSearch:
    def __init__(self,
                 employer_type_name: str = Query(
                     ...,
                     description="The NAME of the employer type to search\n\n"
                                 "**Note:** must be a string with a length of more than 3 characters",
                     min_length=3
                 ),
                 max_results: Optional[PositiveInt] = Query(
                     None,
                     description="The total amount of the employer types matching search parameters to fetch\n\n"
                                 "**Note:** must be a positive integer",
                 )):
        self.employer_type_name = employer_type_name
        self.max_results = max_results
