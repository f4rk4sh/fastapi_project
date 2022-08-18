from typing import List, Optional

from fastapi import Path, Query
from pydantic import BaseModel, Field, PositiveInt, validator

from app import crud
# ToDo unique name
# from app.core.exceptions.common_exceptions import HTTPBadRequestException


class StatusTypeBase(BaseModel):
    name: str = Field(
        ...,
        title="The NAME of the status type",
        description="Note: must be a string with a length of less than 50 characters",
        example="not active",
        max_length=50
    )


class StatusTypeCreate(StatusTypeBase):
    # @validator("name")
    # def unique_name(cls, status_type_name: str) -> str:
    #     status_type = crud.status_type.get_by_name(status_type_name)
    #     if status_type:
    #         raise HTTPBadRequestException(detail="Status type with this name already exists")
    #     return status_type_name
    pass


class StatusTypeUpdate(StatusTypeBase):
    id: PositiveInt = Field(
        ...,
        title="The ID of the status type",
        description="Note: must be a positive integer",
        example=1
    )


class StatusTypeResponse(StatusTypeBase):
    id: PositiveInt = Field(
        ...,
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


class StatusTypeGet:
    def __init__(self,
                 status_type_id: PositiveInt = Path(
                     description="The ID of the status type to fetch\n\n"
                                 "**Note:** must be a positive integer")
                 ):
        self.status_type_id = status_type_id


class StatusTypeDelete:
    def __init__(self,
                 status_type_id: PositiveInt = Path(
                     description="The ID of the status type to delete\n\n"
                                 "**Note:** must be a positive integer")
                 ):
        self.status_type_id = status_type_id


class StatusTypeSearch:
    def __init__(self,
                 status_type_name: str = Query(
                     ...,
                     description="The NAME of the status type to search\n\n"
                                 "**Note:** must be a string with a length of more than 3 characters",
                     min_length=3
                 ),
                 max_results: Optional[PositiveInt] = Query(
                     None,
                     description="The total amount of the status types matching search parameters to fetch\n\n"
                                 "**Note:** must be a positive integer",
                 )):
        self.status_type_name = status_type_name
        self.max_results = max_results
