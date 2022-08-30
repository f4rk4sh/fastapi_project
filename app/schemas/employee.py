from typing import Optional, List

from pydantic import BaseModel, Field, PastDate, PositiveInt


# from app.schemas.user import UserBase, UserCreate, UserUpdate, UserResponse


class EmployeeBase(BaseModel):
    # user: UserBase
    fullname: str = Field(
        title="The FULLNAME of the employee",
        description="Note: must be a string with a length of less than 100 characters",
        example="John Doe",
        max_length=100
    )
    passport: Optional[str] = Field(
        title="The PASSPORT of the employee",
        description="Note: must be a string with a length of less than 50 characters",
        example="AA012345",
        max_length=50
    )
    tax_id: Optional[str] = Field(
        title="The TAX ID of the employee",
        description="Note: must be a string with a length of less than 50 characters",
        example="1234567890",
        max_length=50
    )
    birth_date: Optional[PastDate] = Field(
        title="The DATE of birth of the employee",
        description="Note: must be a date in past with format: yyyy-mm-dd",
        example="1980-01-01"
    )
    employer_id: PositiveInt = Field(
        title="The ID of the employer",
        description="Note: must be a positive integer",
        example=1
    )


class EmployeeCreate(EmployeeBase):
    # ToDo add email validator
    # user: UserCreate
    pass


class EmployeeUpdate(EmployeeBase):
    # ToDo add email validator
    id: PositiveInt = Field(
        title="The ID of the employee",
        description="Note: must be a positive integer",
        example=1
    )
    # user: UserUpdate


class EmployeeResponse(EmployeeBase):
    id: PositiveInt = Field(
        title="The ID of the employee",
        description="Note: must be a positive integer",
        example=1
    )
    # user: UserResponse

    class Config:
        orm_mode = True


class EmployeesResponse(BaseModel):
    employees: List[EmployeeResponse] = Field(
        title="The list of the employees"
    )


class EmployeeSearchResponse(BaseModel):
    results: List[EmployeeResponse] = Field(
        title="The list of the employees matching search parameters"
    )
