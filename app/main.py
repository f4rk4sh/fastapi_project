from fastapi import FastAPI

from app.api.api_enrollment import router
from app.core.documentation.openapi_schema import get_openapi_schema

app = FastAPI()

app.include_router(router)

app.openapi_schema = get_openapi_schema(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
