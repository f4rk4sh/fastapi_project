from fastapi import Path, Query


class RoleParamsDescription:
    """
    Get role parameters description
    """
    @property
    def get_id(self):
        return Path(
            description="The ID of the role to fetch\n\n"
                        "**Note:** must be a positive integer"
        )

    @property
    def delete_id(self):
        return Path(
            description="The ID of the role to delete\n\n"
                        "**Note:** must be a positive integer"
        )

    @property
    def search_parameter(self):
        return Query(
            description="The search parameter of the role\n\n"
                        "**Note:** must be a string with a length of more than 3 characters",
            min_length=3
        )

    @property
    def search_keyword(self):
        return Query(
            description="The search keyword of the role\n\n"
                        "**Note:** must be a string with a length of more than 3 characters",
            min_length=3
        )

    @property
    def max_results_search(self):
        return Query(
            None,
            description="The total amount of the roles matching search parameters to fetch\n\n"
                        "**Note:** must be a positive integer"
        )


role_params: RoleParamsDescription = RoleParamsDescription()
