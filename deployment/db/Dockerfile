FROM mcr.microsoft.com/mssql/server:2019-latest

ARG SA_PASSWORD
ARG ACCEPT_EULA
ARG MSSQL_PID

ENV SA_PASSWORD $SA_PASSWORD
ENV ACCEPT_EULA $ACCEPT_EULA
ENV MSSQL_PID $MSSQL_PID

WORKDIR /src
COPY . /src

CMD ["/bin/bash", "./deployment/db/entrypoint.sh"]