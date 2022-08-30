from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, PositiveInt, FutureDate
from app.schemas.validators import EmailValidator, PasswordValidator, PhoneNumberValidator


class EmployerBase(BaseModel):
    name: str = Field(
        title="The NAME of the employer",
        description="Note: must be a string with a length of less than 100 characters",
        example="Example Company",
        max_length=100
    )

    email: EmailStr = Field(
        title="The EMAIL of the employer",
        description="Note: must be a valid e-mail address with format: [account name]@[domain name].[domain extension]",
        example="example@mail.com"
    )
    phone: str = Field(
        title="The PHONE NUMBER of the employer",
        description="Note: must be a valid phone number with format: +[country code][phone number]",
        example="+380123456789",
        min_length=13,
        max_length=50
    )
    address: str = Field(
        title="The ADDRESS of the employer",
        description="Note: must be a string with a length of less than 100 characters",
        example="1 STREET st LOCALITY",
        max_length=100
    )
    edrpou: str = Field(
        title="The EDRPOU of the employer",
        description="Note: must be a string with a length of less than 50 characters",
        example="12345678",
        max_length=50
    )
    expire_contract_date: Optional[FutureDate] = Field(
        title="The DATE of the contract expiration",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2022-01-01",
    )
    salary_date: Optional[FutureDate] = Field(
        title="The DATE of the salary",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2022-01-01",
    )
    prepayment_date: Optional[FutureDate] = Field(
        title="The DATE of the prepayment",
        description="Note: must be a date in future with format: yyyy-mm-dd",
        example="2022-01-01",
    )
    employer_type_id: PositiveInt = Field(
        title="The ID of the employer type",
        description="Note: must be a positive integer",
        example="1",
    )


class EmployerCreate(EmployerBase, EmailValidator, PasswordValidator, PhoneNumberValidator):
    password: str = Field(
        ...,
        title="The PASSWORD of employer account",
        description="Note: must be a string with a length of more than 8 and less than 100 characters, "
                    "containing at least 1 uppercase character, "
                    "1 number and 1 special symbol (e.g. !@#$%^&*()-_=+|\\)",
        example="Password1!",
        min_length=8,
        max_length=100
    )


class EmployerUpdate(EmployerBase, EmailValidator, PasswordValidator, PhoneNumberValidator):
    id: PositiveInt = Field(
        title="The ID of the employer",
        description="Note: must be a positive integer",
        example=1
    )
    role_id: PositiveInt = Field(
        title="The ID of the role of the employer",
        description="Note: must be a positive integer",
        example="1",
    )
    status_type_id: PositiveInt = Field(
        title="The ID of the status type of the employer",
        description="Note: must be a positive integer",
        example="1",
    )


class EmployerResponse(EmployerBase):
    id: PositiveInt = Field(
        title="The ID of the employer",
        description="Note: must be a positive integer",
        example=1
    )
    role_id: PositiveInt = Field(
        title="The ID of the role of the employer",
        description="Note: must be a positive integer",
        example="1",
    )
    status_type_id: PositiveInt = Field(
        title="The ID of the status type of the employer",
        description="Note: must be a positive integer",
        example="1",
    )

    class Config:
        orm_mode = True


class EmployersResponse(BaseModel):
    employers: List[EmployerResponse] = Field(
        title="The list of the employers",
    )


class EmployerSearchResponse(BaseModel):
    results: List[EmployerResponse] = Field(
        title="The list of the employers matching search parameters",
    )
