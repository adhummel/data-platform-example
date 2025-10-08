from dagster import Definitions

from .assets.ingestion import gtd_raw_data

defs = Definitions(
    assets=[gtd_raw_data],
)