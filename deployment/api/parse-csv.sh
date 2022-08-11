echo "=== Starting up parsing... ==="

echo "=== Рarsing role.csv... ==="

python /src/app/utils/csv_parser.py /src/app/utils/role.csv

sleep 5

echo "=== Рarsing status_type.csv... ==="

python /src/app/utils/csv_parser.py /src/app/utils/status_type.csv

sleep 5

echo "=== Рarsing employer_type.csv... ==="

python /src/app/utils/csv_parser.py /src/app/utils/employer_type.csv

sleep 5

echo "=== Рarsing employer.csv... ==="

python /src/app/utils/csv_parser.py /src/app/utils/employer.csv

sleep 5

echo "=== Рarsing employee.csv... ==="

python /src/app/utils/csv_parser.py /src/app/utils/employee.csv

echo "=== Parsing successfully completed"