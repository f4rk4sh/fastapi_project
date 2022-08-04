echo "Waiting for MSSQL Server starting up..."

sleep 10

/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "$SA_PASSWORD" -d master -i /src/deployment/db/create.sql