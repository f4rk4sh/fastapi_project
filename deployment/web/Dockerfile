FROM tiangolo/uvicorn-gunicorn-fastapi


ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    ACCEPT_EULA=Y \
    DEBIAN_FRONTEND=noninteractive


RUN apt-get install curl
RUN apt-get install apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN apt-get install mssql-tools unixodbc-dev -y


RUN pip install --ignore-installed "poetry==1.1.14"

WORKDIR /src
COPY poetry.lock pyproject.toml /src/

ADD . /src
WORKDIR /src

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /src

ENTRYPOINT /bin/bash ./deployment/db/entrypoint.sh