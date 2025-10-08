"""
Dagster asset for ingesting Global Terrorism Database (GTD) data.
This is the entry point of our data pipeline.
"""

import os
import pandas as pd
from dagster import asset, AssetExecutionContext, Output, MetadataValue
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_postgres_connection():
    """ Create database connection from environemnt variables. Reads .env file:
    DATABASE_HOST, DATABASE_PORT, etc."""

    db_url= (
        f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}"
        f"@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}"
        f"/{os.getenv('DATABASE_NAME')}"
    )
    create_engine(db_url)


