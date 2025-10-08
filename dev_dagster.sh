set -e

cd ~/Documents/data-platform-example
echo "Starting Dagster..."
poetry run dagster dev -m dagster_project -d . -h 0.0.0.0 -p 3000