FROM postgres:15.1

RUN apt update
RUN apt install wget -y
RUN apt install postgresql-15-postgis-3 -y
RUN apt install postgis -y

ENV POSTGRES_USER=is
ENV POSTGRES_PASSWORD=is
ENV POSTGRES_DB=is

COPY initial_schema.sql /docker-entrypoint-initdb.d/

EXPOSE 5432