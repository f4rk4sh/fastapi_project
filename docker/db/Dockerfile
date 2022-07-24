FROM mcr.microsoft.com/mssql/server:2019-latest

ARG SA_PASSWORD
ARG ACCEPT_EULA
ARG MSSQL_PID

ENV SA_PASSWORD ${SA_PASSWORD?password123!}
ENV ACCEPT_EULA ${ACCEPT_EULA?Y}
ENV MSSQL_PID ${MSSQL_PID?Express}


WORKDIR /src
COPY . /src

CMD ["/bin/bash", "./docker/db/entrypoint.sh"]

