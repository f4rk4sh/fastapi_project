from enum import Enum


class ConstantRole(str, Enum):
    su = "su"
    admin = "admin"
    employer = "employer"
    employee = "employee"
