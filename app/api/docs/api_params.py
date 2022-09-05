from fastapi import Path, Query


class CRUDParamsDescriptions:
    """
    Get OpenAPI parameters descriptions for basic CRUD operations endpoints
    """

    def __init__(self, obj_name: str):
        self.obj_name = obj_name

    @property
    def get_id(self):
        return Path(
            description=f"The ID of the {self.obj_name} to fetch\n\n"
            "**Note:** must be a positive integer"
        )

    @property
    def delete_id(self):
        return Path(
            description=f"The ID of the {self.obj_name} to delete\n\n"
            "**Note:** must be a positive integer"
        )

    @property
    def search_parameter(self):
        return Query(
            description=f"The search parameter of the {self.obj_name}\n\n"
            "**Note:** must be a string with a length of more than 3 characters",
            min_length=3,
        )

    @property
    def search_keyword(self):
        return Query(
            description=f"The search keyword of the {self.obj_name}\n\n"
            "**Note:** must be a string with a length of more than 3 characters",
            min_length=3,
        )

    @property
    def max_results_search(self):
        return Query(
            None,
            description=f"The total amount of the {self.obj_name}s matching search parameters to fetch\n\n"
            "**Note:** must be a positive integer",
        )
