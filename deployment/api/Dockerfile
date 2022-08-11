FROM tiangolo/uvicorn-gunicorn-fastapi

WORKDIR /src/

RUN apt-get install curl
RUN apt-get install apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
ENV ACCEPT_EULA=Y DEBIAN_FRONTEND=noninteractive
RUN apt-get install mssql-tools unixodbc-dev -y

RUN pip install --ignore-installed "poetry==1.1.14"

COPY pyproject.toml poetry.lock /src/

RUN poetry config virtualenvs.create false \
    && poetry install --no-root

COPY . /src
ENV PYTHONPATH=/src

ENTRYPOINT /bin/bash /src/deployment/api/entrypoint.sh