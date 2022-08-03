from pydantic import BaseModel, EmailStr, Field, PositiveInt
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=50)
    phone: str = Field(..., max_length=50)


class UserCreate(UserBase):
    password: str = Field(..., max_length=100)
    role_id: PositiveInt
    status_type_id: PositiveInt


class User(UserCreate):
    id: PositiveInt
    creation_date: datetime
    activation_date: datetime
