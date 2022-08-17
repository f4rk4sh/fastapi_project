from typing import Dict, List

from app.db.models import Base


class GetCRUDDescriptions:
    """
    Get OpenAPI descriptions for basic CRUD operations endpoints
    """
    @classmethod
    def get_crud_descriptions(cls, model: Base, search_keywords: List[str]) -> Dict[str, str]:
        model_name = model.__name__.lower()
        return {
            "fetch_all":
                f"""**Note:** fetch all {model_name}s from the database""",
            "search":
                f"""**Note:** search for {model_name}s in the database based on **{', '.join(search_keywords)}** keyword""",
            "create":
                f"""**Note:** create a new {model_name} in the database""",
            "update":
                f"""**Note:** update the {model_name} in the database""",
            "fetch_one":
                f""" **Note:** fetch a single {model_name} by **ID** from the database""",
            "delete":
                f"""**Note:** delete the {model_name} from the database"""

        }

    def __call__(self, model: Base,  search_keywords: List[str]):
        return self.get_crud_descriptions(model, search_keywords)


get_crud_descriptions: GetCRUDDescriptions = GetCRUDDescriptions()
