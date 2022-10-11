from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, ForeignKey, Integer, String
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

    sessions = relationship(
        "Session",
        backref="user",
        passive_deletes=True,
    )


class StatusType(Base):
    __tablename__ = "status_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)

    users = relationship("User", backref="status_type")


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True)

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
    name = Column(String(50), unique=True)

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

    payment_methods = relationship(
        "PaymentMethod",
        backref="employee",
        passive_deletes=True,
    )
    payments = relationship(
        "Payment",
        backref="employee",
        passive_deletes=True,
    )


class Session(Base):
    __tablename__ = "session"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(400))
    creation_date = Column(DateTime)
    status = Column(String(50))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))


class PaymentMethod(Base):
    __tablename__ = "payment_method"

    id = Column(Integer, primary_key=True, index=True)
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey("employee.id", ondelete="CASCADE"))
    bank_id = Column(Integer, ForeignKey("bank.id", ondelete="CASCADE"))

    payments = relationship(
        "Payment",
        backref="payment_method",
        passive_deletes=True,
    )


class Bank(Base):
    __tablename__ = "bank"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    edrpou = Column(String(50))
    mfo = Column(String(50))
    iban = Column(String(50))
    card = Column(String(50))
    account_type_id = Column(Integer, ForeignKey("account_type.id", ondelete="CASCADE"))

    payment_methods = relationship(
        "PaymentMethod",
        backref="bank",
        passive_deletes=True,
    )


class AccountType(Base):
    __tablename__ = "account_type"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    banks = relationship(
        "Bank",
        backref="account_type",
        passive_deletes=True,
    )


class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(BigInteger)
    creation_date = Column(DateTime)
    execution_date = Column(DateTime)
    employee_id = Column(Integer, ForeignKey("employee.id", ondelete="CASCADE"))
    payment_status_id = Column(Integer, ForeignKey("payment_status.id", ondelete="CASCADE"))
    payment_method_id = Column(Integer, ForeignKey("payment_method.id", ondelete="CASCADE"))


class PaymentStatus(Base):
    __tablename__ = "payment_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))

    payments = relationship(
        "Payment",
        backref="payment_status",
        passive_deletes=True,
    )
