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
./dashboard/run_dashboard.sh
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
- [Dashboard Guide](docs/dashboard.md)
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
