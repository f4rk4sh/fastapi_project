from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.api.docs.api_tags import generate_metadata_tags


class OpenAPISchema:
    @classmethod
    def get_openapi_schema(cls, app: FastAPI):
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title="Fastapi project",
            version="1.0",
            description="The project is intended to be helpful in relationship between employers and employees",
            routes=app.routes,
        )
        openapi_schema["tags"] = generate_metadata_tags()
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    def __call__(self, app: FastAPI):
        return self.get_openapi_schema(app)


get_openapi_schema: OpenAPISchema = OpenAPISchema()
