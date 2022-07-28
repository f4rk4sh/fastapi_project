# fastapi project

## Quick start

- clone it 
- copy `.env.example` to `.env` and fill it with relevant data
- run `docker-compose up`

**pay attention:**
due to temporary problem with containers' starting up delay you need to run `docker-compose up --build` first,
wait until the database container is fully loaded, than stop it by pressing `ctrl+c`  and run `docker-compose up` again 

## Notes

if you want to run this project locally:
- clone it 
- copy `.env.example` to `.env` and fill it with relevant data
- create local mssql database, create user with password, grant all privileges to this user
- fill `SQLALCHEMY_DATABASE_URL` (for local connection) in `app.db.init_db.py` with relevant data
- run `uvicorn app.main:app`

