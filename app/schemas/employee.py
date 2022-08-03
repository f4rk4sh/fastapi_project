from pydantic import Field, PositiveInt
from datetime import date

from app.schemas.user import UserBase, UserCreate, User


class EmployeeBase(UserBase):
    fullname: str = Field(..., max_length=100)
    passport: str = Field(..., max_length=50)
    tax_id: str = Field(..., max_length=50)
    birth_date: date


class EmployeeCreate(EmployeeBase, UserCreate):
    user_id: PositiveInt
    employer_id: PositiveInt


class Employee(EmployeeCreate, User):
    class Config:
        orm_mode = True


class EmployeeUpdate(EmployeeBase, User):
    employer_id: PositiveInt

    class Config:
        orm_mode = True
