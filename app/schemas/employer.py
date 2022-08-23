from datetime import date
from typing import Optional, List

from fastapi import Path, Query
from pydantic import BaseModel, EmailStr, Field, PositiveInt


class EmployerBase(BaseModel):
    name: str = Field(
        ...,
        title="The NAME of the employer",
        description="Note: must be a string with a length of less than 100 characters",
        example="Example Company",
        max_length=100
    )

    email: EmailStr = Field(
        ...,
        title="The EMAIL of the employer",
        description="Note: must be a valid e-mail address with format: [account name]@[domain name].[domain extension]",
        example="example@mail.com"
    )
    phone: str = Field(
        ...,
        title="The PHONE NUMBER of the employer",
        description="Note: must be a valid phone number with format: +[country code][phone number]",
        example="+380123456789",
        max_length=50
    )
    # ToDo ?setting role automatically in the corresponding endpoint
    role_id: PositiveInt = Field(
        ...,
        title="The ID of the role of the employer",
        description="Note: must be a positive integer",
        example="1",
    )
    # ToDo ?setting status type automatically in the corresponding endpoint
    status_type_id: PositiveInt = Field(
        ...,
        title="The ID of the status type of the employer",
        description="Note: must be a positive integer",
        example="1",
    )
    address: str = Field(
        ...,
        title="The ADDRESS of the employer",
        description="Note: must be a string with a length of less than 100 characters",
        example="1 STREET st LOCALITY",
        max_length=100
    )
    edrpou: str = Field(
        ...,
        title="The EDRPOU of the employer",
        description="Note: must be a string with a length of less than 50 characters",
        example="12345678",
        max_length=50
    )
    expire_contract_date: Optional[date] = Field(
        title="The DATE of the contract expiration",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2022-01-01",
    )
    salary_date: Optional[date] = Field(
        title="The DATE of the salary",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2022-01-01",
    )
    prepayment_date: Optional[date] = Field(
        title="The DATE of the prepayment",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2022-01-01",
    )
    employer_type_id: PositiveInt = Field(
        ...,
        title="The ID of the employer type",
        description="Note: must be a positive integer",
        example="1",
    )


class EmployerCreate(EmployerBase):
    password: str = Field(
        ...,
        title="The PASSWORD of employer account",
        description="Note: must be a string with a length of more than 10 and less than 100 characters, "
                    "containing at least 1 uppercase character, 1 number and 1 special symbol",
        example="Password1!",
    )
    pass
    # ToDo email, phone number, password, dates validators


class EmployerUpdate(EmployerBase):
    id: PositiveInt = Field(
        ...,
        title="The ID of the employer",
        description="Note: must be a positive integer",
        example=1
    )


class EmployerResponse(EmployerBase):
    id: PositiveInt = Field(
        ...,
        title="The ID of the employer",
        description="Note: must be a positive integer",
        example=1
    )

    class Config:
        orm_mode = True


class EmployersResponse(BaseModel):
    employers: List[EmployerResponse] = Field(
        title="The list of the employers",
        alias="employers"
    )


class EmployerSearchResponse(BaseModel):
    results: List[EmployerResponse] = Field(
        title="The list of the employers matching search parameters",
        alias="results"
    )


class EmployerGet:
    def __init__(self,
                 employer_id: PositiveInt = Path(
                     description="The ID of the employer to fetch\n\n"
                                 "**Note:** must be a positive integer")
                 ):
        self.employer_id = employer_id


class EmployerDelete:
    def __init__(self,
                 employer_id: PositiveInt = Path(
                     description="The ID of the employer to delete\n\n"
                                 "**Note:** must be a positive integer")
                 ):
        self.employer_id = employer_id


class EmployerSearch:
    def __init__(self,
                 employer_name: str = Query(
                     ...,
                     description="The NAME of the employer to search\n\n"
                                 "**Note:** must be a string with a length of more than 3 characters",
                     min_length=3
                 ),
                 max_results: Optional[PositiveInt] = Query(
                     None,
                     description="The total amount of the employers matching search parameters to fetch\n\n"
                                 "**Note:** must be a positive integer",
                 )):
        self.employer_name = employer_name
        self.max_results = max_results
