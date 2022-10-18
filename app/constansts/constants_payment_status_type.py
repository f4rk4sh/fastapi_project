from enum import Enum


class ConstantPaymentStatusType(str, Enum):
    success = "success"
    in_process = "in_process"
    error = "error"
