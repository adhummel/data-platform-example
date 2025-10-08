#!/bin/bash

# Modern Data Platform - Automated Setup Script (GTD Version)
# Run this script to initialize the complete project structure

set -e  # Exit on error

echo "🚀 Setting up Modern Data Platform - GTD Edition..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Create main directories
echo -e "${BLUE}📁 Creating directory structure...${NC}"

directories=(
    "dagster_project/assets"
    "dagster_project/resources"
    "dagster_project/schedules"
    "dagster_project/sensors"
    "dbt_project/models/raw"
    "dbt_project/models/stg"
    "dbt_project/models/int"
    "dbt_project/models/marts"
    "dbt_project/macros"
    "dbt_project/tests"
    "dbt_project/seeds"
    "data/raw"
    "data/processed"
    "data/seeds"
    "notebooks"
    "dashboard/pages"
    "dashboard/utils"
    "scripts"
    "tests"
    "docs"
    "diagrams"
)

for dir in "${directories[@]}"; do
    mkdir -p "$dir"
    echo "  ✓ Created $dir"
done

# Create __init__.py files for Python packages
echo ""
echo -e "${BLUE}🐍 Creating Python package files...${NC}"

init_files=(
    "dagster_project/__init__.py"
    "dagster_project/assets/__init__.py"
    "dagster_project/resources/__init__.py"
    "dagster_project/schedules/__init__.py"
    "dagster_project/sensors/__init__.py"
    "dashboard/__init__.py"
    "dashboard/utils/__init__.py"
    "tests/__init__.py"
)

for file in "${init_files[@]}"; do
    touch "$file"
    echo "  ✓ Created $file"
done

# Create .gitignore
echo ""
echo -e "${BLUE}📝 Creating configuration files...${NC}"

cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
.venv
*.egg-info/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment
.env
.env.local

# Data (GTD data should not be committed due to terms of use)
data/raw/*
data/processed/*
*.csv
*.xlsx
*.parquet
!data/seeds/*.csv

# dbt
dbt_project/logs/
dbt_project/target/
dbt_project/dbt_packages/

# Dagster
dagster_home/
.dagster/

# OS
.DS_Store
Thumbs.db

# Notebooks
.ipynb_checkpoints/

# Streamlit
.streamlit/
EOF

echo "  ✓ Created .gitignore"

# Create .env.example
cat > .env.example << 'EOF'
# Database Configuration
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=geopolitical_platform
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres

# Snowflake (Optional - for production)
SNOWFLAKE_ACCOUNT=
SNOWFLAKE_USER=
SNOWFLAKE_PASSWORD=
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=GEOPOLITICAL_DATA
SNOWFLAKE_SCHEMA=PUBLIC

# GTD Data Configuration
# Note: GTD data requires manual download from START consortium
# https://www.start.umd.edu/gtd/contact/
GTD_DATA_PATH=data/raw/globalterrorismdb.xlsx

# Additional Data Sources (Optional)
ACLED_API_KEY=
UCDP_DATA_PATH=

# Dagster Configuration
DAGSTER_HOME=~/.dagster
EOF

echo "  ✓ Created .env.example"

# Create docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: geopolitical_data_db
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: geopolitical_platform
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
EOF

echo "  ✓ Created docker-compose.yml"

# Create requirements.txt
cat > requirements.txt << 'EOF'
# Orchestration
dagster==1.7.0
dagster-webserver==1.7.0
dagster-postgres==0.23.0
dagster-dbt==0.23.0

# Transformation
dbt-core==1.7.0
dbt-postgres==1.7.0

# Data Processing
pandas==2.2.0
numpy==1.26.0
pyarrow==15.0.0
openpyxl==3.1.2

# Database
sqlalchemy==2.0.25
psycopg2-binary==2.9.9

# API & Data Sources
requests==2.31.0

# Geospatial (optional for mapping)
geopandas==0.14.0
folium==0.15.0

# Visualization
streamlit==1.31.0
plotly==5.18.0

# Development
pytest==8.0.0
black==24.1.0
ruff==0.2.0
jupyter==1.0.0
python-dotenv==1.0.0
EOF

echo "  ✓ Created requirements.txt"

# Create pyproject.toml for Poetry
cat > pyproject.toml << 'EOF'
[tool.poetry]
name = "geopolitical-data-platform"
version = "0.1.0"
description = "Modern data platform for geopolitical and conflict analysis with Dagster, dbt, and Streamlit"
authors = ["Your Name <your.email@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.9"
dagster = "^1.7.0"
dagster-webserver = "^1.7.0"
dagster-postgres = "^0.23.0"
dagster-dbt = "^0.23.0"
dbt-core = "^1.7.0"
dbt-postgres = "^1.7.0"
pandas = "^2.2.0"
numpy = "^1.26.0"
pyarrow = "^15.0.0"
openpyxl = "^3.1.2"
sqlalchemy = "^2.0.25"
psycopg2-binary = "^2.9.9"
requests = "^2.31.0"
geopandas = "^0.14.0"
folium = "^0.15.0"
streamlit = "^1.31.0"
plotly = "^5.18.0"
python-dotenv = "^1.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^8.0.0"
black = "^24.1.0"
ruff = "^0.2.0"
jupyter = "^1.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ['py39']

[tool.ruff]
line-length = 88
target-version = "py39"
EOF

echo "  ✓ Created pyproject.toml"

# Create basic Dagster workspace.yaml
cat > dagster_project/workspace.yaml << 'EOF'
load_from:
  - python_module:
      module_name: dagster_project
      working_directory: .
EOF

echo "  ✓ Created dagster_project/workspace.yaml"

# Create basic dbt_project.yml
cat > dbt_project/dbt_project.yml << 'EOF'
name: 'geopolitical_platform'
version: '1.0.0'
config-version: 2

profile: 'geopolitical_platform'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

clean-targets:
  - "target"
  - "dbt_packages"
  - "logs"

models:
  geopolitical_platform:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: view
      +schema: intermediate
    marts:
      +materialized: table
      +schema: marts
EOF

echo "  ✓ Created dbt_project/dbt_project.yml"

# Create dbt profiles.yml
cat > dbt_project/profiles.yml << 'EOF'
geopolitical_platform:
  target: dev
  outputs:
    dev:
      type: postgres
      host: "{{ env_var('DATABASE_HOST', 'localhost') }}"
      port: "{{ env_var('DATABASE_PORT', 5432) | as_number }}"
      user: "{{ env_var('DATABASE_USER', 'postgres') }}"
      password: "{{ env_var('DATABASE_PASSWORD', 'postgres') }}"
      dbname: "{{ env_var('DATABASE_NAME', 'geopolitical_platform') }}"
      schema: public
      threads: 4
      keepalives_idle: 0
EOF

echo "  ✓ Created dbt_project/profiles.yml"

# Create starter README
cat > README.md << 'EOF'
# Geopolitical Data Platform 🌍

> End-to-end ELT pipeline for geopolitical and conflict analysis using Dagster, dbt, PostgreSQL, and Streamlit

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![dbt](https://img.shields.io/badge/dbt-1.7+-orange.svg)](https://www.getdbt.com/)
[![Dagster](https://img.shields.io/badge/dagster-latest-purple.svg)](https://dagster.io/)

---

## 📊 Project Overview

This project implements a **production-ready data platform** for analyzing global terrorism and conflict data using the **Global Terrorism Database (GTD)** from START consortium.

### Key Features
- **Ingests** GTD data (200k+ incidents from 1970-present)
- **Transforms** raw data into analytics-ready models using dbt
- **Orchestrates** the entire pipeline with Dagster
- **Visualizes** geopolitical insights through an interactive Streamlit dashboard

**Use Cases**: 
- Conflict trend analysis
- Attack pattern identification
- Regional threat assessment
- Temporal analysis of terrorism evolution
- Target and weapon type analysis

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Docker (for PostgreSQL)
- Git
- GTD Data Access (see Data Acquisition below)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/geopolitical-data-platform.git
cd geopolitical-data-platform
```

2. **Set up Python environment**
```bash
# Using Poetry (recommended)
poetry install

# OR using pip
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Start PostgreSQL**
```bash
docker-compose up -d
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your credentials
```

5. **Acquire GTD data** (see Data Acquisition section below)

6. **Initialize database**
```bash
python scripts/setup_database.py
```

7. **Run the pipeline**
```bash
# Start Dagster UI
dagster dev

# In another terminal, materialize assets
dagster asset materialize --select '*'
```

8. **Launch dashboard**
```bash
streamlit run dashboard/app.py
```

---

## 📥 Data Acquisition

### Global Terrorism Database (GTD)

The GTD is maintained by START (National Consortium for the Study of Terrorism and Responses to Terrorism) at the University of Maryland.

**To obtain the data:**

1. Visit: https://www.start.umd.edu/gtd/contact/
2. Complete the data request form
3. Download the Excel file (globalterrorismdb.xlsx)
4. Place it in `data/raw/globalterrorismdb.xlsx`

**Data Overview:**
- 200,000+ terrorist incidents (1970-2020)
- 135+ variables per incident
- Geographic coverage: worldwide
- Regular updates from START consortium

**Key Fields:**
- Date/time, location (country, region, city, coordinates)
- Attack characteristics (type, success, suicide)
- Weapon types, target types
- Casualties (killed, wounded)
- Perpetrator groups

---

## 🏗️ Architecture

```
┌─────────────────┐       ┌──────────────┐       ┌─────────────────┐
│   GTD Dataset   │──────▶│   Dagster    │──────▶│   PostgreSQL/   │
│  (Excel/CSV)    │       │ Orchestrator │       │   Snowflake     │
└─────────────────┘       └──────────────┘       └─────────────────┘
                                 │                         │
                                 │                         │
                                 ▼                         ▼
                          ┌──────────────┐       ┌─────────────────┐
                          │     dbt      │──────▶│    Streamlit    │
                          │ Transformations      │    Dashboard    │
                          └──────────────┘       └─────────────────┘
```

### Tech Stack
- **Orchestration**: Dagster (asset-based orchestration)
- **Transformation**: dbt (dimensional modeling)
- **Warehouse**: PostgreSQL (dev) → Snowflake (prod)
- **Visualization**: Streamlit + Plotly
- **Language**: Python 3.9+

---

## 🔄 Data Pipeline

### 1. Ingestion Layer
- Reads GTD Excel file
- Validates data quality
- Loads to `raw_data.gtd_incidents` table
- Handles incremental loads

### 2. Transformation Layer (dbt)

**Staging Models** (`models/staging/`)
- `stg_gtd_incidents`: Clean and standardize incident records
- `stg_gtd_locations`: Geocoded location data
- `stg_gtd_groups`: Perpetrator group information

**Intermediate Models** (`models/intermediate/`)
- `int_incidents_enriched`: Join incidents with location and group context
- `int_casualties_aggregated`: Calculate casualty metrics
- `int_temporal_features`: Extract temporal patterns

**Mart Models** (`models/marts/`)
- `fct_incidents`: Fact table with all incidents and metrics
- `dim_locations`: Location dimension (country, region, city)
- `dim_groups`: Perpetrator group dimension
- `dim_attack_types`: Attack methodology dimension
- `metrics_regional`: Regional aggregated metrics
- `metrics_temporal`: Time-series metrics

### 3. Orchestration Layer (Dagster)
- Scheduled daily runs for new data
- Asset-based dependency management
- Data quality checks
- Automatic retries and alerting
- Full lineage tracking

### 4. Visualization Layer
**Key Dashboards**:
- Global incident heatmap
- Temporal trends (incidents/casualties over time)
- Regional breakdowns (Middle East, South Asia, etc.)
- Attack type analysis
- Perpetrator group profiles
- Target analysis (government, civilian, military)

---

## 📈 Sample Analytics Questions

This platform can answer questions like:

- What are the global trends in terrorism incidents from 1970-2020?
- Which regions have seen the most significant increase/decrease in attacks?
- What are the most common attack types by region?
- How have casualty rates evolved over time?
- Which terrorist groups are most active in specific regions?
- What are the most frequently targeted entities?
- How do attack patterns differ between urban and rural areas?
- What is the success rate of different attack methodologies?

---

## 🧪 Testing

```bash
# Run dbt tests
cd dbt_project
dbt test

# Run Python tests
pytest tests/

# Run data quality checks
dbt test --select tag:quality
```

---

## 📚 Documentation

- [Architecture Deep Dive](docs/architecture.md)
- [Data Dictionary](docs/data_dictionary.md)
- [Dagster Setup Guide](docs/dagster_guide.md)
- [GTD Field Reference](docs/gtd_fields.md)
- [dbt Model Documentation](http://localhost:8080) - Run `dbt docs serve`

---

## 🚧 Roadmap

- [x] GTD data ingestion
- [x] Core dbt models (staging → marts)
- [x] Dagster orchestration
- [ ] Snowflake integration
- [ ] Add ACLED data (Armed Conflict Location & Event Data)
- [ ] Add UCDP data (Uppsala Conflict Data Program)
- [ ] Implement data contracts (dbt contracts + Dagster checks)
- [ ] Geographic visualization (Folium maps)
- [ ] Predictive analytics (conflict forecasting)
- [ ] CI/CD pipeline
- [ ] Deploy to cloud (AWS/GCP)

---

## 🔒 Data Ethics & Security

**Important Considerations:**

- This data contains sensitive information about violent events
- Use responsibly and ethically for research/analysis purposes only
- Respect GTD terms of use (non-commercial research use)
- Implement appropriate access controls in production
- Consider data anonymization for public-facing applications
- Follow your organization's data governance policies

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Add tests for new features
4. Submit a Pull Request

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file for details

**Data License**: GTD data usage must comply with START consortium terms

---

## 🙏 Acknowledgments

- START consortium (University of Maryland) for GTD data
- National Consortium for the Study of Terrorism and Responses to Terrorism
- Dagster, dbt, and Streamlit communities

---

## 📞 Contact

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [yourprofile](https://linkedin.com/in/yourprofile)

---

**⭐ If this project helped you understand modern data platforms, please give it a star!**
EOF

echo "  ✓ Created README.md"

# Create starter scripts
cat > scripts/setup_database.py << 'EOF'
"""Initialize database schemas and tables."""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    """Create necessary schemas in the database."""
    db_url = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    
    engine = create_engine(db_url)
    
    schemas = ['raw_data', 'staging', 'intermediate', 'marts']
    
    with engine.connect() as conn:
        for schema in schemas:
            conn.execute(text(f"CREATE SCHEMA IF NOT EXISTS {schema}"))
            print(f"✓ Created schema: {schema}")
        conn.commit()
    
    print("\n✅ Database setup complete!")
    print("\n📋 Next steps:")
    print("  1. Download GTD data from https://www.start.umd.edu/gtd/contact/")
    print("  2. Place the file at: data/raw/globalterrorismdb.xlsx")
    print("  3. Run: dagster dev")

if __name__ == "__main__":
    setup_database()
EOF

chmod +x scripts/setup_database.py
echo "  ✓ Created scripts/setup_database.py"

# Create GTD data download guide
cat > scripts/download_gtd_data.md << 'EOF'
# GTD Data Acquisition Guide

## Step 1: Request Access

1. Visit the GTD website: https://www.start.umd.edu/gtd/contact/
2. Fill out the data request form with:
   - Your name and email
   - Institution (can be "Independent Researcher")
   - Purpose: "Academic research and data platform development"
3. Agree to terms of use (non-commercial research)

## Step 2: Download Data

1. You'll receive download link via email (usually within 24 hours)
2. Download the Excel file: `globalterrorismdb_YYYY_Jan2023.xlsx`
3. File size: ~200MB

## Step 3: Place Data

```bash
# Create directory if needed
mkdir -p data/raw

# Move downloaded file
mv ~/Downloads/globalterrorismdb_*.xlsx data/raw/globalterrorismdb.xlsx
```

## Alternative: Sample Dataset

For initial development/testing, you can create a sample dataset:

```python
# Run this to create a sample GTD dataset
python scripts/create_sample_gtd.py
```

## Data Structure Preview

The GTD Excel file contains:
- **Sheet 1**: Main incident data (200k+ rows, 135+ columns)
- Key fields: eventid, iyear, imonth, iday, country_txt, region_txt, 
  city, latitude, longitude, attacktype1_txt, targtype1_txt, 
  weaptype1_txt, nkill, nwound, gname, summary

## Data Quality Notes

- Some incidents have missing coordinates
- Casualty counts may be estimates
- Group attribution can be uncertain
- Always check the 'doubtterr' field for uncertain classifications
EOF

echo "  ✓ Created scripts/download_gtd_data.md"

# Create docs files
cat > docs/architecture.md << 'EOF'
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
EOF

echo "  ✓ Created docs/architecture.md"

cat > docs/data_dictionary.md << 'EOF'
# Data Dictionary

## Source Data: Global Terrorism Database

### Key Fields from GTD

| Field | Type | Description |
|-------|------|-------------|
| eventid | TEXT | Unique incident identifier |
| iyear | INTEGER | Year of incident |
| imonth | INTEGER | Month of incident (1-12) |
| iday | INTEGER | Day of incident (1-31) |
| country_txt | TEXT | Country name |
| region_txt | TEXT | Geographic region |
| city | TEXT | City name |
| latitude | NUMERIC | Latitude coordinate |
| longitude | NUMERIC | Longitude coordinate |
| attacktype1_txt | TEXT | Primary attack type |
| targtype1_txt | TEXT | Primary target type |
| weaptype1_txt | TEXT | Primary weapon type |
| nkill | INTEGER | Number killed |
| nwound | INTEGER | Number wounded |
| gname | TEXT | Perpetrator group name |
| summary | TEXT | Incident description |

## Marts Layer

### fct_incidents
Fact table containing all terrorism incidents.

| Column | Type | Description |
|--------|------|-------------|
| incident_id | TEXT | Unique incident identifier |
| incident_date | DATE | Date of incident |
| location_key | TEXT | FK to dim_locations |
| group_key | TEXT | FK to dim_groups |
| attack_type_key | TEXT | FK to dim_attack_types |
| target_type | TEXT | Primary target category |
| weapon_type | TEXT | Primary weapon used |
| casualties_killed | INTEGER | Number of fatalities |
| casualties_wounded | INTEGER | Number of injuries |
| total_casualties | INTEGER | Total killed + wounded |
| is_suicide | BOOLEAN | Suicide attack indicator |
| is_success | BOOLEAN | Attack success indicator |

### dim_locations
Dimension table for geographic locations.

| Column | Type | Description |
|--------|------|-------------|
| location_key | TEXT | Surrogate key |
| country | TEXT | Country name |
| region | TEXT | Geographic region |
| city | TEXT | City name |
| latitude | NUMERIC | Latitude |
| longitude | NUMERIC | Longitude |

### dim_groups
Dimension table for perpetrator groups.

| Column | Type | Description |
|--------|------|-------------|
| group_key | TEXT | Surrogate key |
| group_name | TEXT | Organization name |
| first_attack_date | DATE | First recorded attack |
| last_attack_date | DATE | Most recent attack |
| total_attacks | INTEGER | Number of attacks |
| total_casualties | INTEGER | Total casualties caused |

### metrics_regional
Regional aggregated metrics.

| Column | Type | Description |
|--------|------|-------------|
| region | TEXT | Geographic region |
| year | INTEGER | Year |
| incident_count | INTEGER | Number of incidents |
| total_killed | INTEGER | Total fatalities |
| total_wounded | INTEGER | Total injuries |
| avg_casualties_per_incident | NUMERIC | Average casualties |
EOF

echo "  ✓ Created docs/data_dictionary.md"

cat > docs/gtd_fields.md << 'EOF'
# GTD Field Reference

## Essential Fields for Analysis

### Temporal
- `iyear`, `imonth`, `iday`: Date components
- `date`: Formatted date string

### Geographic
- `country`, `country_txt`: Country code and name
- `region`, `region_txt`: Region code and name
- `provstate`: Province/state
- `city`: City name
- `latitude`, `longitude`: Coordinates

### Incident Characteristics
- `attacktype1_txt`: Attack methodology
- `targtype1_txt`: Target category
- `weaptype1_txt`: Weapon category
- `success`: Attack success (1=yes, 0=no)
- `suicide`: Suicide attack (1=yes, 0=no)

### Casualties
- `nkill`: Number killed
- `nwound`: Number wounded
- `nkillus`, `nwoundus`: US casualties
- `nkillter`, `nwoundte`: Terrorist casualties

### Perpetrators
- `gname`: Group name
- `gsubname`: Group subname
- `gname2`, `gname3`: Additional groups (if multiple)

### Details
- `summary`: Incident description
- `motive`: Stated motive
- `weapdetail`: Weapon details
- `target1`: Specific target entity

## Data Quality Indicators
- `doubtterr`: Doubt about terrorism classification
- `multiple`: Part of coordinated attack
- `ishostkid`: Hostage/kidnapping involved
EOF

echo "  ✓ Created docs/gtd_fields.md"

# Git initialization
echo ""
echo -e "${BLUE}🔧 Initializing Git repository...${NC}"
if [ ! -d .git ]; then
    git init
    git branch -M main
    echo "  ✓ Git repository initialized"
else
    echo "  ℹ Git repository already exists"
fi

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "📋 Next Steps:"
echo "  1. Copy environment file: cp .env.example .env"
echo "  2. Start PostgreSQL: docker-compose up -d"
echo "  3. Install dependencies: poetry install (or pip install -r requirements.txt)"
echo "  4. Set up database: python scripts/setup_database.py"
echo "  5. Download GTD data: See scripts/download_gtd_data.md"
echo "  6. Start Dagster: dagster dev"
echo ""
echo "📚 Documentation:"
echo "  - README.md - Project overview"
echo "  - docs/architecture.md - System design"
echo "  - docs/data_dictionary.md - Data definitions"
echo "  - docs/gtd_fields.md - GTD field reference"
echo "  - scripts/download_gtd_data.md - Data acquisition guide"
echo ""
echo "🎉 Happy building!"