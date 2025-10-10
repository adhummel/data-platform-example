# 🌍 Global Terrorism Database - Threat Intelligence Dashboard

A professional analytics platform built with Streamlit for analyzing global terrorism data and answering critical intelligence questions.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL database running
- dbt models successfully built

### Launch the Dashboard

```bash
# Option 1: Use the launcher script (recommended)
./run_dashboard.sh

# Option 2: Manual launch
pip install -r requirements.txt
streamlit run dashboard.py
```

### Access
Open your browser to **http://localhost:8501**

## 🎯 Dashboard Features

### **Executive Summary**
- Real-time threat metrics and KPIs
- Critical hotspot alerts
- Quick overview visualizations

### **🗺️ Hotspot Intelligence**
*Where are terrorism hotspots emerging over time?*
- Interactive global heatmap with intensity scores
- Threat level classifications (Critical, High, Moderate, Low)
- Trend analysis (Accelerating, Stable, Declining)

### **📈 Group Expansion Tracking**
*What groups are expanding their operational reach fastest?*
- Expansion velocity metrics (countries/year)
- Recent expansion trends (5-year window)
- Geographic reach analysis

### **🌐 Cross-Border Networks**
*Which countries face the most cross-border terrorism spillovers?*
- Interactive network graph linking source and target countries
- Spillover risk index choropleth map
- Source diversity analysis

### **🔮 Predictive Analytics**
*Can we predict where and when the next attack might occur?*
- Time series trend analysis
- Risk scoring based on momentum and volatility
- High-risk country identification

### **🧬 Behavioral Clustering**
*Are there clusters of groups with similar behavioral patterns?*
- 3D K-means clustering visualization
- Behavioral archetype classification
- Tactical preference analysis

## 📊 Data Requirements

The dashboard expects the following mart tables in your database:

- `dbt_marts.emerging_hotspots` - Hotspot analysis with intensity scores
- `dbt_marts.group_expansion` - Group expansion velocity metrics
- `dbt_marts.cross_border_risk` - Cross-border spillover risk analysis
- `dbt_marts.forecasting_dataset` - Predictive features and time series
- `dbt_marts.group_clustering_features` - Behavioral clustering features

These are automatically created when you run `dbt run` in the dbt_project directory.

## 🔧 Configuration

### Database Connection
Ensure your `.env` file contains:
```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=geopolitical_platform
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
```

### Caching
- Data queries are cached for 10 minutes (600 seconds)
- Clear cache from the Streamlit UI: "☰" menu → "Clear cache"

## 🛠️ Troubleshooting

### Database Connection Issues
```bash
# Test database connection
psql -h localhost -U postgres -d geopolitical_platform

# Verify environment variables
cat .env
```

### Missing Tables
```bash
# Run dbt to materialize marts
cd dbt_project
dbt run --select marts
```

### Import Errors
```bash
# Install requirements
pip install -r requirements.txt
```

## 📈 Key Metrics

| Metric | Description |
|--------|-------------|
| **Hotspot Intensity Score** | 0-100 scale measuring threat concentration |
| **Expansion Velocity** | Countries/year expansion rate |
| **Spillover Risk Score** | Cross-border threat index |
| **Threat Level** | Critical → High → Moderate → Low |

## 💡 Tips

1. Use tab navigation to switch between analysis modules
2. Hover over visualizations for detailed tooltips
3. Data is cached - subsequent loads are faster
4. Export charts using Plotly's download button (📷)
5. Clear cache with the "C" key to refresh data

## 🎨 Visualizations

- **Scatter Geo Maps** - Hotspot heatmap with zoom and pan
- **Choropleth Maps** - Spillover risk index by country
- **3D Scatter Plots** - Behavioral clustering in feature space
- **Network Graphs** - Cross-border terrorism flows
- **Time Series** - Trend analysis and forecasting
- **Bar Charts** - Rankings and comparisons

## 🎯 Use Cases

### Intelligence Analysts
- Monitor emerging threat zones
- Track terrorist organization expansion
- Identify cross-border spillover patterns

### Policy Makers
- Assess regional stability
- Allocate security resources
- Evaluate counter-terrorism effectiveness

### Researchers
- Study behavioral patterns
- Analyze temporal trends
- Build predictive models

---

**Data Source:** Global Terrorism Database (START Consortium)
**Built with:** Streamlit, Plotly, dbt, PostgreSQL
