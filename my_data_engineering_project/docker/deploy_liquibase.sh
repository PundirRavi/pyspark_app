#!/bin/bash
set -e

# Required environment variables:
# LIQUIBASE_CHANGELOG - path to changelog file inside container
# JDBC_URL - JDBC connection URL (Snowflake)
# JDBC_USERNAME - DB username
# JDBC_PASSWORD - DB password
# JDBC_DRIVER - JDBC driver class name

echo "Starting Liquibase deployment..."
liquibase \
  --changeLogFile="$LIQUIBASE_CHANGELOG" \
  --url="$JDBC_URL" \
  --username="$JDBC_USERNAME" \
  --password="$JDBC_PASSWORD" \
  --driver="$JDBC_DRIVER" \
  update

echo "Liquibase deployment complete."
