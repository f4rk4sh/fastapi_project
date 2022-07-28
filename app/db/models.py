from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date
from sqlalchemy.orm import relationship

from .init_db import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    phone = Column(String(50))
    creation_date = Column(DateTime)
    activation_date = Column(DateTime)
    role_id = Column(Integer, ForeignKey("role.id"))
    status_type_id = Column(Integer, ForeignKey("status_type.id"))

    role = relationship("Role", back_populates="users")
    status_type = relationship("StatusType", back_populates="users")
    employers = relationship("Employer", back_populates="user")
    employees = relationship("Employee", back_populates="user")


class StatusType(Base):
    __tablename__ = "status_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    users = relationship("User", back_populates="status_type")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    users = relationship("User", back_populates="role")


class Employer(Base):
    __tablename__ = "employer"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String(100))
    edrpou = Column(String(50), index=True)
    expire_contract_date = Column(Date)
    salary_date = Column(Date)
    prepayment_date = Column(Date)
    user_id = Column(Integer, ForeignKey("user.id"))
    employer_type_id = Column(Integer, ForeignKey("employer_type.id"))

    user = relationship("User", back_populates="employers")
    employer_type = relationship("EmployerType", back_populates="employers")
    employees = relationship("Employee", back_populates="employer")


class EmployerType(Base):
    __tablename__ = "employer_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    employers = relationship("Employer", back_populates="employer_type")


class Employee(Base):
    __tablename__ = "employee"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100))
    passport = Column(String(50), index=True)
    tax_id = Column(String(50), index=True)
    birth_date = Column(Date)
    user_id = Column(Integer, ForeignKey("user.id"))
    employer_id = Column(Integer, ForeignKey("employer.id"))

    user = relationship("User", back_populates="employees")
    employer = relationship("Employer", back_populates="employees")


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(100))
    creation_date = Column(DateTime)
