from fastapi import FastAPI, APIRouter, status

from app.api.api_enrollment import api_router
from app.db import models
from app.db.session import engine

root_router = APIRouter()
app = FastAPI(title="Fastapi project")

models.Base.metadata.create_all(bind=engine)  # will be removed after adding flyway


@root_router.get("/", status_code=status.HTTP_200_OK)
def root() -> dict:
    return {"Hello": "World!"}


app.include_router(root_router)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
