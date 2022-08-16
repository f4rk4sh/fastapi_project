FROM flyway/flyway:latest-alpine

COPY ./deployment/migrations/versions/*.sql /flyway/sql/
COPY ./deployment/migrations/flyway.conf /flyway/conf/

ENTRYPOINT flyway migrate