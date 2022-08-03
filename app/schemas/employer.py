from pydantic import Field, PositiveInt
from datetime import date

from app.schemas.user import UserBase, UserCreate, User


class EmployerBase(UserBase):
    address: str = Field(..., max_length=100)
    edrpou: str = Field(..., max_length=50)
    expire_contract_date: date
    salary_date: date
    prepayment_date: date


class EmployerCreate(EmployerBase, UserCreate):
    user_id: PositiveInt
    employer_type_id: PositiveInt


class Employer(EmployerCreate, User):
    class Config:
        orm_mode = True


class EmployeeUpdate(EmployerBase, User):
    employer_type_id: PositiveInt

    class Config:
        orm_mode = True
