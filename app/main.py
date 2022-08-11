from fastapi import FastAPI

from app.api.api_enrollment import router

app = FastAPI(title="Fastapi project")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
