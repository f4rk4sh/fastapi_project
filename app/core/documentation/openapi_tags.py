from typing import List, Dict, Any

from app.db.models import Base, Role
from app.schemas.tag import MetadataTag


def metadata_tags() -> List[Dict[str, Any]]:
    """
    Get OpenAPI tags
    """
    return get_crud_tags([Role])


def get_crud_tag_name(model: Base) -> str:
    """
    Get OpenAPI tag name for basic CRUD operations endpoints
    """
    return get_crud_tag(model).name


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


class GetCRUDTags:
    """
    Get OpenAPI tags for basic CRUD operations endpoints
    """
    @classmethod
    def get_crud_tags(cls, models: List[Base]) -> List[Dict[str, Any]]:
        return [tag.dict(by_alias=True) for tag in [get_crud_tag(model) for model in models]]

    def __call__(self, models: List[Base]):
        return self.get_crud_tags(models)


get_crud_tag: GetCRUDTag = GetCRUDTag()
get_crud_tags: GetCRUDTags = GetCRUDTags()
