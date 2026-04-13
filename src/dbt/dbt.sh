#!/bin/bash
# Wrapper script to run dbt using Docker instead of local python installation
# Usage: ./dbt.sh run
#        ./dbt.sh test

DBT_IMAGE="ghcr.io/dbt-labs/dbt-postgres:1.5.2"

echo "Running dbt using Docker ($DBT_IMAGE)..."
docker run --rm \
  --network dwh_dwh_network \
  -v "$(pwd)":/usr/app \
  -w /usr/app \
  $DBT_IMAGE "$@" --profiles-dir .
