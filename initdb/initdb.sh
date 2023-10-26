#!/bin/bash
set -e

if psql -U postgres -d postgres -c "SELECT 1 FROM pg_database WHERE datname = 'task_tracker'" | grep -qw 1; then
  echo "База данных 'task_tracker' уже существует. Пропустить создание."
else
  psql -U postgres <<-EOSQL
    CREATE DATABASE task_tracker;
EOSQL
  echo "База данных 'task_tracker' создана."
fi

if psql -U postgres -tAc "SELECT 1 FROM pg_user WHERE usename = 'task_tracker_user'" | grep -qw 1; then
  echo "Пользователь 'task_tracker_user' уже существует. Пропустить создание."
else
  psql -U postgres -d task_tracker <<-EOSQL
    CREATE USER task_tracker_user WITH PASSWORD '123';
    CREATE SCHEMA task_tracker_schema;
    ALTER SCHEMA task_tracker_schema OWNER TO task_tracker_user;
    ALTER DATABASE task_tracker OWNER TO task_tracker_user;
EOSQL
  echo "Пользователь 'task_tracker_user' и схема 'task_tracker_schema' созданы."
fi
