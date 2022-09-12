from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    phone = Column(String(50))
    creation_date = Column(DateTime)
    activation_date = Column(DateTime, nullable=True)
    role_id = Column(Integer, ForeignKey("role.id"))
    status_type_id = Column(Integer, ForeignKey("status_type.id"))

    employer = relationship(
        "Employer",
        uselist=False,
        single_parent=True,
        backref="user",
        passive_deletes=True,
    )
    employee = relationship(
        "Employee",
        uselist=False,
        single_parent=True,
        backref="user",
        passive_deletes=True,
    )

    sessions = relationship("Session", backref="user")


class StatusType(Base):
    __tablename__ = "status_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    users = relationship("User", backref="status_type")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    users = relationship("User", backref="role")


class Employer(Base):
    __tablename__ = "employer"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    address = Column(String(100))
    edrpou = Column(String(50), index=True)
    expire_contract_date = Column(Date, nullable=True)
    salary_date = Column(Date, nullable=True)
    prepayment_date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    employer_type_id = Column(Integer, ForeignKey("employer_type.id"))

    employees = relationship("Employee", backref="employer")


class EmployerType(Base):
    __tablename__ = "employer_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    employers = relationship("Employer", backref="employer_type")


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100))
    passport = Column(String(50), index=True, nullable=True)
    tax_id = Column(String(50), index=True, nullable=True)
    birth_date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    employer_id = Column(Integer, ForeignKey("employer.id"))


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(500))
    creation_date = Column(DateTime)
    expiration_date = Column(DateTime)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
