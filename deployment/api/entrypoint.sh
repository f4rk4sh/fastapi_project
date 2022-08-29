echo  "=== Waiting for database initialization... ==="

sleep 10

echo "=== Starting up project... ==="

uvicorn app.main:app --host 0.0.0.0 --reload