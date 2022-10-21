from enum import Enum


class ConstantAccountType(str, Enum):
    card = "card"
    iban = "iban"
