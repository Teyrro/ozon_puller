#!/bin/bash

set -e
set -u


function create_user_and_database() {
	local database=$1
	echo "  Creating user and database '$database'"
	psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
	    CREATE DATABASE $database;
EOSQL
}

if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
	echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
	for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
		create_user_and_database $db
	done
	echo "Multiple databases created"
fi

#function create_database() {
#  database=$1
##  user=$2
##  password=$3
##with password '$password'
#  echo "Creating user and database '$database'"
#  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
#    CREATE DATABASE $database;
#
#EOSQL
#}
##    CREATE USER $user with encrypted password '$password';
##    GRANT CREATE ON SCHEMA public TO $user;
##    GRANT ALL PRIVILEGES ON DATABASE $database TO $user;
#
#
## POSTGRES_MULTIPLE_DATABASES=db1,db2
## POSTGRES_MULTIPLE_DATABASES=db1,password,db2
#if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
#  echo "Multiple database creation requested:  $POSTGRES_MULTIPLE_DATABASES"
#  for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr "," " "); do
#    db_name=$(echo $db | awk -F":" '{print $1}')
##    user=$(echo $db | awk -F":" '{print $2}')
##    pswd=$(echo $db | awk -F":" '{print $3}')
##    if [[ -z "$pswd" ]]
##    then
##      pswd=$user
##    fi
#
##    echo "user is '$user', pass is '$pswd' and db_name is '$db_name'"
#    echo "db_name is '$db_name'"
## $user $pswd
#    create_database $db_name
#  done
#  echo "Multiple databases created!"
#fi