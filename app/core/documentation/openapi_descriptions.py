from typing import List

from app.db.models import Base


class CRUDDescriptions:
    """
    Get OpenAPI descriptions for basic CRUD operations endpoints
    """
    def __init__(self, model: Base, search_parameters: List[str]):
        model_name = model.__name__.lower()
        self.fetch_all = f"""**Note:** fetch all {model_name}s from the database"""
        self.search = f"""**Note:** search for {model_name}s in the database based on **{', '.join(search_parameters)}** parameter"""
        self.create = f"""**Note:** create a new {model_name} in the database"""
        self.update = f"""**Note:** update the {model_name} in the database"""
        self.fetch_one = f""" **Note:** fetch a single {model_name} by **ID** from the database"""
        self.delete = f"""**Note:** delete the {model_name} from the database"""
