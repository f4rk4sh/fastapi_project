from enum import Enum


class ConstantSessionStatus(str, Enum):
    logged_in = "logged-in"
    logged_out = "logged-out"
