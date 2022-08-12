echo  "=== Waiting for database initialization... ==="

sleep 10

echo  "=== Inserting basic data to the database... ==="

python /src/app/utils/csv_parser.py

echo "=== Starting up project... ==="

uvicorn app.main:app --host 0.0.0.0 --reload