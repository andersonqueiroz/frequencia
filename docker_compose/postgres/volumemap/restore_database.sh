#!/bin/bash

echo "DROP DATABASE db_frequencia; CREATE DATABASE db_frequencia;" | psql
PGPASSWORD=postgres pg_restore --verbose -U postgres -d db_frequencia -Fc frequencia.dump