import re

from fastapi import HTTPException, status
from pydantic import BaseModel, validator
from sqlalchemy.orm import Session

from app.db.get_database import get_db
from app.db.models import User

db: Session = next(get_db())


class UserValidators(BaseModel):
    @validator("email", check_fields=False)
    def email_validator(cls, email: str) -> str:
        user = db.query(User).filter(User.email == email).first()
        if user:
            # ToDo will be HTTPBadRequestException after merging documentation pull request
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account with this email already exists")
        return email

    @validator("password", check_fields=False)
    def password_validator(cls, password: str) -> str:
        if not re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+|\\])[\s\S]{8,100}$", password):
            # ToDo will be HTTPBadRequestException after merging documentation pull request
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least 1 uppercase letter, "
                       "1 number and 1 special symbol (e.g. !@#$%^&*()-_=+|\\)")
        return password

    @validator("phone", check_fields=False)
    def phone_validator(cls, phone: str) -> str:
        if not re.match(r"^\+\d{12}$", phone):
            # ToDo will be HTTPBadRequestException after merging documentation pull request
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Phone number must be in the format: +[country code][phone number]")
        return phone
