sleep 15s

/opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P password123! -d master -i /src/docker/db/create.sql