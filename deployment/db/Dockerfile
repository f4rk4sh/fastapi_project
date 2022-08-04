FROM mcr.microsoft.com/mssql/server:2019-latest

WORKDIR /src
COPY . /src

ENTRYPOINT /bin/bash /src/deployment/db/entrypoint.sh