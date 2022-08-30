import re

from pydantic import BaseModel, validator, root_validator
from sqlalchemy.orm import Session

from app.core.exceptions.common_exceptions import HTTPBadRequestException
from app.db.get_database import get_db
from app.db.models import User


class EmailValidator(BaseModel):
    @root_validator()
    def email_validator(cls, values) -> str:
        db: Session = next(get_db())
        user_data = values.get("user")
        obj_id = values.get("id")
        user = db.query(User).filter(User.email == user_data.email).first()
        if user:
            if user.employer:
                if user.employer.id == obj_id:
                    return values
            elif user.employee:
                if user.employee.id == obj_id:
                    return values
            raise HTTPBadRequestException(detail="Account with this email already exists")
        return values


class PasswordValidator(BaseModel):
    @validator("password", check_fields=False)
    def password_validator(cls, password: str) -> str:
        if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+|\\])[\s\S]{8,100}$", password):
            raise HTTPBadRequestException(
                detail="Password must contain at least 1 uppercase letter, "
                       "1 number and 1 special symbol (e.g. !@#$%^&*()-_=+|\\)"
            )
        return password


class PhoneNumberValidator(BaseModel):
    @validator("phone", check_fields=False)
    def phone_validator(cls, phone: str) -> str:
        if not re.match(r"^\+\d{12}$", phone):
            raise HTTPBadRequestException(
                detail="Phone number must be in the format: +[country code][phone number]"
            )
        return phone
