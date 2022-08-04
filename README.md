# fastapi project

## Quick start

- clone it 
- copy `.env.example` to `.env` and fill it with relevant data
- run `docker-compose up`

## Notes

if you want to run this project locally:
- clone it 
- copy `.env.example` to `.env` and fill it with relevant data
- create local mssql database, create user with password, grant all privileges to this user
- fill `SQLALCHEMY_DATABASE_URL` in `app/core/config/db_config.py` with relevant data
- use `SQLALCHEMY_DATABASE_URL` (for local connection) in `app/db/session.py`
- run `uvicorn app.main:app`

