echo "=== Waiting for MSSQL Server starting up... ==="

for i in {1..50};
do
    /opt/mssql-tools/bin/sqlcmd -S "${DB_HOST}" -U "${DB_USER}" -P "${MSSQL_SA_PASSWORD}" -d master -i /src/deployment/db/setup_sql_server.sql
    if [ $? -eq 0 ]
    then
        echo "=== MSSQL Server starting up completed ==="
        break
    else
        echo "=== MSSQL Server starting up not completed yet... ==="
        sleep 1
    fi
done