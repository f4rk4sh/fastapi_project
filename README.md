# fastapi project

This project is intended to be helpful in relationship between employer and employees by providing system of salary payment.

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
- run `uvicorn app.main:app`
