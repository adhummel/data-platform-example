from pathlib import Path
from dagster import Definitions
from dagster_dbt import DbtCliResource

from .assets.ingestion import gtd_raw_data
from .assets.dbt_assets import geopolitical_dbt_assets, DBT_PROJECT_DIR

# Create dbt CLI resource
dbt_resource = DbtCliResource(project_dir=DBT_PROJECT_DIR)

defs = Definitions(
    assets=[gtd_raw_data, geopolitical_dbt_assets],
    resources={
        "dbt": dbt_resource,
    },
)