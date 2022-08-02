from fastapi import FastAPI, APIRouter, status

from app.api.api_enrollment import router
from app.db import models
from app.db.session import engine

app = FastAPI(title="Fastapi project")

models.Base.metadata.create_all(bind=engine)  # will be removed after adding flyway

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
