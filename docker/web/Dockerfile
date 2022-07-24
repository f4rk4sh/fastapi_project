FROM python:3.9

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.14

RUN pip install --ignore-installed "poetry==$POETRY_VERSION"

WORKDIR /src
COPY poetry.lock pyproject.toml /src/

ADD . /src
WORKDIR /src

RUN poetry config virtualenvs.create false \
  && poetry install --no-interaction --no-ansi

COPY . /src