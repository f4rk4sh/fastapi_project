import re
from typing import Any, Dict, List

from app.db.models import (AccountType, Bank, Base, Employee, EmployeeAccount,
                           Employer, EmployerPaymentMethod, EmployerType,
                           PaymentHistory, PaymentStatusType, Role, StatusType)
from app.schemas.schema_tag import MetadataTag


def generate_metadata_tags() -> List[Dict[str, Any]]:
    """
    Get OpenAPI tags
    """
    tags = [
        get_crud_tag(model)
        for model in [
            AccountType,
            Bank,
            Employee,
            EmployeeAccount,
            Employer,
            EmployerPaymentMethod,
            EmployerType,
            PaymentStatusType,
            Role,
            StatusType,
        ]
    ]
    tags.append(get_crud_tag(PaymentHistory, operations=["read"]))
    return [tag.dict(by_alias=True) for tag in sorted(tags, key=lambda tag: tag.name)]


class GetCRUDTag:
    """
    Get OpenAPI tag for basic CRUD operations endpoints
    """

    @classmethod
    def get_crud_tag(cls, model: Base, operations: List[str]) -> MetadataTag:
        name = " ".join(re.findall(r"[A-Z][^A-Z]*", model.__name__))
        crud_operations = (
            ", ".join([operation.capitalize() for operation in operations])
            if operations
            else "CRUD"
        )
        return MetadataTag(
            name=f"{name}",
            description=f"Endpoints to support **{crud_operations}** operations with **{name}**",
        )

    def __call__(self, model: Base, operations: List[str] = None):
        return self.get_crud_tag(model, operations)


get_crud_tag: GetCRUDTag = GetCRUDTag()
