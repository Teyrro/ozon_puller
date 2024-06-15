FROM postgres

COPY init_multiple_databases.sh /docker-entrypoint-initdb.d/

RUN chmod +x /docker-entrypoint-initdb.d/init_multiple_databases.sh

EXPOSE 5432
