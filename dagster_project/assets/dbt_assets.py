"""
Dagster assets for dbt models.
This file defines all dbt models as Dagster assets using dagster-dbt integration.
"""

import os
from pathlib import Path
from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

# Get the dbt project directory
DBT_PROJECT_DIR = Path(__file__).resolve().parents[2] / "dbt_project"
MANIFEST_PATH = DBT_PROJECT_DIR / "target" / "manifest.json"


@dbt_assets(
    manifest=MANIFEST_PATH,
)
def geopolitical_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """
    All dbt models, seeds, and snapshots as Dagster assets.

    This includes:
    - raw.raw_gtd (raw layer)
    - staging models (stg_attack_*)
    - intermediate models (int layer)
    - marts models (final layer)
    """
    yield from dbt.cli(["build"], context=context).stream()
