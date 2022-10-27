import re
from typing import Any, Dict, List

from app.db.models import AccountType, Bank, Base, Employee, Employer, EmployerType, PaymentStatusType, Role, StatusType

from app.schemas.schema_tag import MetadataTag


def generate_metadata_tags() -> List[Dict[str, Any]]:
    """
    Get OpenAPI tags
    """
    return [
        tag.dict(by_alias=True)
        for tag in [
            get_crud_tag(model) for model in [
                AccountType, Bank, Employee, Employer, EmployerType, PaymentStatusType, Role, StatusType
            ]
        ]
    ]


class GetCRUDTag:
    """
    Get OpenAPI tag for basic CRUD operations endpoints
    """

    @classmethod
    def get_crud_tag(cls, model: Base) -> MetadataTag:
        name = " ".join(re.findall(r"[A-Z][^A-Z]*", model.__name__))
        return MetadataTag(
            name=f"{name}s",
            description=f"Endpoints to support all the **CRUD (Create, Read, Update, Delete)** operations with **{name}s**",
        )

    def __call__(self, model: Base):
        return self.get_crud_tag(model)


get_crud_tag: GetCRUDTag = GetCRUDTag()
