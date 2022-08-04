echo  "Waiting for database initialization..."

sleep 20

uvicorn app.main:app --host 0.0.0.0 --reload