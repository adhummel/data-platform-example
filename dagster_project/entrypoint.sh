#!/bin/bash
set -e

echo "================================================"
echo "Dagster Entrypoint: Preparing environment"
echo "================================================"

# Wait for postgres to be ready
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h ${DATABASE_HOST:-postgres} -p ${DATABASE_PORT:-5432} -U ${DATABASE_USER:-postgres}; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 2
done
echo "✓ PostgreSQL is ready"

# Generate dbt manifest
echo "Generating dbt manifest..."
cd /app/dbt_project

# First, install any dbt dependencies (packages)
if [ -f "packages.yml" ]; then
  echo "Installing dbt packages..."
  dbt deps --profiles-dir . || echo "Warning: dbt deps failed, continuing anyway"
fi

# Parse the dbt project to generate manifest.json
echo "Parsing dbt project..."
dbt parse --profiles-dir . || {
  echo "Error: Failed to generate dbt manifest"
  exit 1
}

if [ -f "target/manifest.json" ]; then
  echo "✓ dbt manifest generated successfully at target/manifest.json"
  echo "  Size: $(du -h target/manifest.json | cut -f1)"
else
  echo "ERROR: manifest.json was not created!"
  exit 1
fi

cd /app

echo "================================================"
echo "Starting Dagster: $@"
echo "================================================"

# Execute the command passed to docker (e.g., dagster dev)
exec "$@"
