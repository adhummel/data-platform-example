# Global Terrorism Analytics Platform

A production-grade data platform for analyzing global terrorism patterns, built with modern data engineering tools and best practices. This project demonstrates end-to-end ELT pipeline development, dimensional modeling, and analytical dashboard creation using real-world geopolitical data.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![dbt](https://img.shields.io/badge/dbt-1.7+-orange.svg)](https://www.getdbt.com/)
[![Dagster](https://img.shields.io/badge/dagster-1.7+-purple.svg)](https://dagster.io/)

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Data Models](#data-models)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Analytics Capabilities](#analytics-capabilities)
- [Development](#development)
- [Documentation](#documentation)

## Overview

### Purpose

This platform ingests, transforms, and analyzes the Global Terrorism Database (GTD) to provide actionable insights into terrorism patterns, trends, and risk factors. The system is designed to answer critical analytical questions about:

- Geographic hotspot emergence and intensity
- Terrorist group expansion patterns and velocity
- Cross-border spillover risks and network effects
- Predictive risk factors and temporal trends
- Behavioral clustering of terrorist organizations

### Data Source

**Global Terrorism Database (GTD)**
- **Provider**: START Consortium, University of Maryland
- **Coverage**: 200,000+ incidents from 1970 to present
- **Scope**: Worldwide terrorism events with 135+ attributes per incident
- **Update Frequency**: Annual releases
- **Access**: Available via data request at https://www.start.umd.edu/gtd/

### Key Features

- **Automated Data Pipeline**: Orchestrated ingestion and transformation via Dagster
- **Dimensional Data Models**: Star schema design with dbt for analytical queries
- **Interactive Dashboard**: Streamlit-based visualization layer with 6 analytical modules
- **Scalable Architecture**: Containerized services with Docker Compose
- **Data Quality**: Automated testing and validation at each pipeline stage
- **Full Lineage Tracking**: Complete data lineage from source to dashboard

## Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Sources                              │
│                   GTD Excel File (200k+ rows)                    │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Ingestion Layer (Dagster)                      │
│  • Reads GTD Excel file                                          │
│  • Data validation and cleansing                                 │
│  • Loads to PostgreSQL raw schema                                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                Transformation Layer (dbt)                        │
│                                                                   │
│  Raw Layer                                                        │
│  └─ data_raw.gtd_incidents (source table)                        │
│                                                                   │
│  Staging Layer                                                    │
│  ├─ stg_attack_location                                          │
│  ├─ stg_attack_actors                                            │
│  ├─ stg_attack_weapons                                           │
│  ├─ stg_attack_targets                                           │
│  └─ stg_attack_results                                           │
│                                                                   │
│  Intermediate Layer                                              │
│  ├─ int_gtd_enriched (base enrichment)                          │
│  ├─ int_cross_border_flows                                      │
│  ├─ int_spatial_hotspots                                        │
│  ├─ int_group_expansion_tracking                                │
│  ├─ int_predictive_features                                     │
│  └─ int_region_time_series                                      │
│                                                                   │
│  Marts Layer                                                     │
│  ├─ emerging_hotspots                                           │
│  ├─ group_expansion                                             │
│  ├─ cross_border_risk                                           │
│  ├─ forecasting_dataset                                         │
│  └─ group_clustering_features                                   │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Analytics Layer (Streamlit)                      │
│  • Executive Summary Dashboard                                   │
│  • Hotspot Intelligence                                          │
│  • Group Expansion Analysis                                      │
│  • Cross-Border Networks                                         │
│  • Predictive Analytics                                          │
│  • Behavioral Clustering                                         │
└─────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Orchestration** | Dagster 1.7 | Asset-based pipeline orchestration, scheduling, monitoring |
| **Transformation** | dbt 1.7 | SQL-based data transformation, testing, documentation |
| **Database** | PostgreSQL 15 | OLAP data warehouse for analytical queries |
| **Visualization** | Streamlit | Interactive dashboard and data exploration |
| **Analytics** | Python, Pandas, NumPy | Data processing and feature engineering |
| **ML Libraries** | scikit-learn, NetworkX | Clustering analysis and network graphs |
| **Containerization** | Docker, Docker Compose | Service orchestration and deployment |
| **Data Visualization** | Plotly | Interactive charts and maps |

## Data Models

### Analytical Marts

The platform produces five key analytical marts, each optimized for specific use cases:

#### 1. Emerging Hotspots (`dbt_marts.emerging_hotspots`)
Identifies and scores geographic regions with concentrated terrorism activity.

**Key Metrics:**
- Hotspot intensity score (0-100)
- Recent incident counts (trailing 3 years)
- Year-over-year trend direction
- Threat level classification (Critical/High/Moderate/Low)
- Active terrorist group count

**Use Case:** Monitor emerging threat zones and allocate security resources

#### 2. Group Expansion (`dbt_marts.group_expansion`)
Tracks terrorist organization geographic expansion over time.

**Key Metrics:**
- Expansion velocity (countries per year)
- Total countries operated
- Recent expansion activity (5-year window)
- Years active
- Threat classification

**Use Case:** Identify rapidly expanding organizations requiring counter-terrorism focus

#### 3. Cross-Border Risk (`dbt_marts.cross_border_risk`)
Analyzes terrorism spillover patterns across national borders.

**Key Metrics:**
- Spillover risk score (composite metric)
- Source country diversity
- Total spillover attacks
- Shared terrorist groups
- Average time to spillover

**Use Case:** Assess regional stability and cross-border security cooperation needs

#### 4. Forecasting Dataset (`dbt_marts.forecasting_dataset`)
Time-series features for predictive modeling of future incidents.

**Key Metrics:**
- Incident momentum (3-year moving average)
- Volatility indicators
- Prior year spike detection
- Lagged casualty counts
- Active group tracking

**Use Case:** Build machine learning models for risk forecasting

#### 5. Group Clustering Features (`dbt_marts.group_clustering_features`)
Behavioral feature set for terrorist organization segmentation.

**Key Metrics:**
- Normalized attack volume, lethality, geographic reach
- Suicide attack rate
- Success rate
- Weapon preferences (explosives, firearms)
- Target preferences (government, civilian)

**Use Case:** Understand terrorist group archetypes and tactical patterns

### Data Modeling Approach

The project follows **dimensional modeling** best practices:

- **Layered Architecture**: Raw → Staging → Intermediate → Marts
- **Staging Models**: One-to-one with source, type casting and basic cleansing
- **Intermediate Models**: Complex business logic, feature engineering
- **Marts**: Denormalized, analytics-ready tables optimized for query performance
- **Incremental Logic**: Designed for efficient daily refreshes
- **Testing**: Schema tests, unique/not-null constraints, referential integrity

## Getting Started

### Prerequisites

- **Python 3.9+**
- **Docker & Docker Compose**
- **Git**
- **GTD Data Access** (see Data Acquisition section)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd data-platform-example
```

2. **Set up environment**
```bash
# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

Example `.env`:
```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=geopolitical_platform
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
GTD_DATA_PATH=data/raw/globalterrorismdb_0522dist.xlsx
```

4. **Acquire GTD data**
- Visit https://www.start.umd.edu/gtd/contact/
- Complete data request form
- Download Excel file
- Place in `data/raw/globalterrorismdb_0522dist.xlsx`

5. **Start infrastructure**
```bash
# Start PostgreSQL
docker-compose up -d postgres

# Verify database is healthy
docker-compose ps
```

6. **Initialize database**
```bash
python scripts/setup_database.py
```

### Running the Pipeline

#### Option 1: Local Development

```bash
# Start Dagster UI
dagster dev -f dagster_project

# In Dagster UI (http://localhost:3000):
# 1. Navigate to Assets
# 2. Click "Materialize all"
# Or materialize specific assets
```

#### Option 2: Docker Compose (Production-like)

```bash
# Start all services
docker-compose up -d

# Access Dagster UI at http://localhost:3000
# Materialize assets through the UI
```

### Launching the Dashboard

```bash
# From project root
./dashboard/run_dashboard.sh

# Or manually
cd dashboard
streamlit run dashboard.py

# Access at http://localhost:8501
```

## Usage

### Running dbt Transformations

```bash
cd dbt_project

# Run all models
dbt run

# Run specific layer
dbt run --select staging
dbt run --select marts

# Run specific model
dbt run --select emerging_hotspots

# Test data quality
dbt test

# Generate documentation
dbt docs generate
dbt docs serve  # Access at http://localhost:8080
```

### Dagster Operations

```bash
# Launch Dagster UI
dagster dev

# Materialize all assets
dagster asset materialize --select '*'

# Materialize specific asset
dagster asset materialize --select gtd_raw_data

# Run with sensors/schedules
dagster-daemon run
```

### Dashboard Features

The Streamlit dashboard provides six analytical modules:

1. **Executive Summary**: High-level metrics and KPIs
2. **Hotspot Intelligence**: Geographic heat maps and intensity scoring
3. **Group Expansion**: Organization growth tracking and velocity analysis
4. **Cross-Border Networks**: Network graphs and spillover risk maps
5. **Predictive Analytics**: Time-series trends and risk forecasting
6. **Behavioral Clustering**: K-means clustering and tactical pattern analysis

## Project Structure

```
.
├── dagster_project/          # Orchestration layer
│   ├── assets/
│   │   ├── ingestion.py      # GTD data ingestion asset
│   │   └── dbt_assets.py     # dbt transformation assets
│   ├── resources/            # Database connections
│   ├── schedules/            # Scheduled runs
│   └── sensors/              # Event-driven triggers
│
├── dbt_project/              # Transformation layer
│   ├── models/
│   │   ├── raw/              # Source definitions
│   │   ├── staging/          # Cleaned, typed models
│   │   ├── int/              # Intermediate business logic
│   │   └── marts/            # Analytics-ready tables
│   ├── tests/                # Data quality tests
│   └── macros/               # Reusable SQL functions
│
├── dashboard/                # Visualization layer
│   ├── dashboard.py          # Streamlit application
│   ├── .streamlit/           # Dashboard configuration
│   └── run_dashboard.sh      # Launch script
│
├── scripts/                  # Utility scripts
│   └── setup_database.py     # Database initialization
│
├── tests/                    # Unit and integration tests
│   └── test_dashboard_connection.py
│
├── docs/                     # Documentation
│   ├── architecture.md       # System design details
│   ├── data_dictionary.md    # Field definitions
│   ├── dashboard.md          # Dashboard user guide
│   └── gtd_fields.md         # GTD schema reference
│
├── data/                     # Data directory (gitignored)
│   └── raw/                  # Source data files
│
├── docker-compose.yml        # Service orchestration
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

## Analytics Capabilities

### Questions This Platform Answers

**Geographic Analysis:**
- Where are terrorism hotspots emerging over time?
- Which regions show accelerating or declining trends?
- What is the geographic distribution of different attack types?

**Organizational Intelligence:**
- Which terrorist groups are expanding their operational reach fastest?
- How do groups differ in tactics, lethality, and targeting?
- What are the behavioral patterns of high-threat organizations?

**Cross-Border Dynamics:**
- Which countries face the greatest spillover risks?
- What are the network effects between perpetrator and victim countries?
- How do shared terrorist groups affect regional security?

**Predictive Analytics:**
- What are the leading indicators of increased terrorism risk?
- Which countries show high momentum and volatility?
- How do casualty rates correlate with incident frequency?

**Behavioral Patterns:**
- Are there distinct terrorist group archetypes?
- How do weapon and target preferences cluster?
- What tactical patterns emerge from unsupervised learning?

## Development

### Running Tests

```bash
# dbt tests
cd dbt_project
dbt test

# Python unit tests
pytest tests/

# Dashboard connection test
python tests/test_dashboard_connection.py
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .
```

### Adding New Models

1. Create SQL file in appropriate dbt directory
2. Add schema documentation in `schema.yml`
3. Write tests for data quality
4. Update mart dependencies in Dagster
5. Add visualizations to dashboard if applicable

## Documentation

Comprehensive documentation is available in the `/docs` directory:

- **[Architecture Guide](docs/architecture.md)**: Detailed system design and data flow
- **[Data Dictionary](docs/data_dictionary.md)**: Complete field definitions and business logic
- **[Dashboard Guide](docs/dashboard.md)**: User manual for the analytics dashboard
- **[GTD Fields Reference](docs/gtd_fields.md)**: Source data schema and field descriptions

Generate dbt documentation:
```bash
cd dbt_project
dbt docs generate
dbt docs serve
```

## Data Ethics and Security

### Important Considerations

This platform processes sensitive information about violent events. Users must:

- **Use Responsibly**: For research, analysis, and security purposes only
- **Respect Terms of Use**: Comply with GTD data usage restrictions (non-commercial research)
- **Implement Access Controls**: Secure sensitive data in production environments
- **Consider Privacy**: Anonymize data for public-facing applications
- **Follow Governance**: Adhere to organizational data policies and regulations

### Security Best Practices

- Never commit `.env` files or credentials to version control
- Use role-based access control (RBAC) in production databases
- Implement SSL/TLS for database connections
- Regularly audit data access logs
- Apply data retention policies per compliance requirements

## Roadmap

### Current Status

- [x] GTD data ingestion pipeline
- [x] Dimensional data models (staging → marts)
- [x] Dagster orchestration and monitoring
- [x] Interactive Streamlit dashboard
- [x] Docker containerization
- [x] Data quality testing framework

### Future Enhancements

- [ ] Cloud deployment (AWS/GCP/Azure)
- [ ] Snowflake integration for production warehouse
- [ ] Additional data sources (ACLED, UCDP conflict data)
- [ ] Machine learning models for prediction
- [ ] CI/CD pipeline with GitHub Actions
- [ ] dbt contracts for data contracts enforcement
- [ ] Advanced geographic visualizations (Folium maps)
- [ ] API layer for programmatic access
- [ ] Real-time data ingestion capabilities

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Write tests for new functionality
4. Ensure all tests pass (`pytest tests/ && dbt test`)
5. Submit a pull request with clear description

## License

This project is licensed under the MIT License. See LICENSE file for details.

**Data License**: GTD data usage must comply with START Consortium terms of use.

## Acknowledgments

- **START Consortium** (University of Maryland) for maintaining the Global Terrorism Database
- **Dagster**, **dbt**, and **Streamlit** communities for excellent open-source tools
- Contributors and maintainers of supporting libraries

## Contact

For questions, issues, or collaboration opportunities:

- **GitHub Issues**: [Project Issues](../../issues)
- **Discussions**: [Project Discussions](../../discussions)

---

**Built with modern data engineering best practices for analytics at scale.**
