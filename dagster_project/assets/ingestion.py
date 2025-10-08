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
    return create_engine(db_url)

@asset(
    description="Raw GTD data loaded from Excel file into PostgreSQL",
    compute_kind="pandas",
    group_name="ingestion",
)
def gtd_raw_data(context: AssetExecutionContext) -> Output:
    """
    Load GTD Excel file and ingest into raw_data schema.
    
    This asset:
    1. Reads the GTD Excel file (200k+ rows)
    2. Selects key columns (50+ fields)
    3. Cleans missing values (GTD uses -9, -99 as null codes)
    4. Loads to PostgreSQL raw_data.gtd_incidents table
    5. Returns metadata about the load
    """
    gtd_file_path = os.getenv('GTD_DATA_PATH', 'data/raw/globalterrorismdb_0522dist.xlsx')
    context.log.info(f"📂 Reading GTD data from: {gtd_file_path}")

    df = pd.read_excel(gtd_file_path, sheet_name=0)
    context.log.info(f"✅ Loaded {len(df):,} rows from GTD file")

    df.columns = df.columns.str.lower().str.replace(' ', '_')

    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].replace([-9, -99, -999], pd.NA)
    context.log.info(f"🔧 Converted GTD missing value codes (-9, -99, -999) to NULL")

    engine = get_postgres_connection()

    context.log.info(f"💾 Writing {len(df.columns)} columns to raw_data.gtd_incidents...")
    context.log.info(f"   This preserves ALL source data for downstream transformations")
    
    df.to_sql(
        name='gtd_incidents',
        schema='raw',
        con=engine,
        if_exists='replace',  # Change to 'append' for incremental loads
        index=False,
        chunksize=5000,  # Write in batches for memory efficiency
        method='multi'  # Faster bulk insert
    )

    context.log.info("✅ Ingestion complete!")
    
    # Simple return (no metadata)
    return Output(
    value=len(df),
    metadata={
        "num_rows": len(df),
        "num_columns": len(df.columns),
        "date_range": f"{int(df['iyear'].min())}-{int(df['iyear'].max())}",
    }
)