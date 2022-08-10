echo  "=== Waiting for database initialization... ==="

sleep 15

uvicorn app.main:app --host 0.0.0.0 --reload