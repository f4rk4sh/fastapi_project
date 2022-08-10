echo "=== Starting up parsing... ==="

python /src/app/utils/csv_parser.py /src/app/utils/role.csv
python /src/app/utils/csv_parser.py /src/app/utils/status_type.csv
python /src/app/utils/csv_parser.py /src/app/utils/employer_type.csv
python /src/app/utils/csv_parser.py /src/app/utils/employer.csv
python /src/app/utils/csv_parser.py /src/app/utils/employee.csv

echo "=== Parsing successfully completed"