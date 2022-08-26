from typing import List, Dict, Any

from app.db.models import Base, Role
from app.schemas.tag import MetadataTag


def generate_metadata_tags() -> List[Dict[str, Any]]:
    """
    Get OpenAPI tags
    """
    return [tag.dict(by_alias=True) for tag in [get_crud_tag(model) for model in [Role]]]


class GetCRUDTag:
    """
    Get OpenAPI tag for basic CRUD operations endpoints
    """
    @classmethod
    def get_crud_tag(cls, model: Base) -> MetadataTag:
        return MetadataTag(
            name=f"{model.__name__}s",
            description=f"Endpoints to support all the **CRUD (Create, Read, Update, Delete)** operations with **{model.__name__}s**"
        )

    def __call__(self, model: Base):
        return self.get_crud_tag(model)


get_crud_tag: GetCRUDTag = GetCRUDTag()
