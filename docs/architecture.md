# Architecture Documentation

## System Overview

This platform analyzes global terrorism and conflict data using modern data engineering practices.

### Data Flow

1. **Ingestion**: GTD Excel file is read and validated
2. **Storage**: Raw data lands in `raw_data.gtd_incidents` table
3. **Transformation**: dbt models create analytical layers
4. **Orchestration**: Dagster schedules and monitors the pipeline
5. **Visualization**: Streamlit dashboard provides interactive analytics

### Technology Stack

- **Orchestration**: Dagster 1.7 (asset-based)
- **Transformation**: dbt Core 1.7 (SQL modeling)
- **Warehouse**: PostgreSQL 15 (dev) / Snowflake (prod)
- **Visualization**: Streamlit + Plotly
- **Language**: Python 3.9+

## Component Details

### Dagster Assets
- `gtd_raw_data`: Ingest GTD Excel file
- `dbt_staging_models`: Run staging transformations
- `dbt_intermediate_models`: Run intermediate transformations
- `dbt_mart_models`: Build analytics tables

### dbt Models

**Staging Layer**
- Clean and standardize raw GTD data
- Handle missing values
- Type conversion and validation

**Intermediate Layer**
- Enrich incidents with location context
- Calculate derived metrics
- Join with reference data

**Mart Layer**
- Dimensional model (facts and dimensions)
- Aggregated metrics tables
- Analytics-optimized structures

### Database Schemas
- `raw_data`: Raw GTD incidents
- `staging`: Cleaned, typed data
- `intermediate`: Business logic applied
- `marts`: Final analytics tables
