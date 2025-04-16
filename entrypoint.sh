#!/bin/bash

echo "⏳ Waiting for PostgreSQL at postgres:5432..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "✅ PostgreSQL is up - continuing..."

airflow db init

airflow users create \
  --username admin \
  --password admin \
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com || true

exec airflow "$@"
