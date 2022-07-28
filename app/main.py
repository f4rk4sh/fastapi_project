import time
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.crud.base import create_user, get_users, get_user_by_email
from app.db import models
from app.db.init_db import SessionLocal, engine
from app.schemas.schema import User, UserCreate


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/', response_model=User)
def user_add(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user=user)


@app.get('/users/', response_model=list[User])
def user_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users
