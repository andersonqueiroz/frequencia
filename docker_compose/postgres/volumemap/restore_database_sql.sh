#!/bin/bash

echo "DROP DATABASE db_frequencia; CREATE DATABASE db_frequencia;" | psql db_frequencia < frequencia.dump
