# 🌍 Global Terrorism Database - Threat Intelligence Dashboard

A sleek, FBI-style analytics platform built with Streamlit for analyzing global terrorism data and answering critical intelligence questions.

## 🎯 Dashboard Features

### **Executive Dashboard**
- Real-time threat metrics and KPIs
- Critical hotspot alerts
- Quick overview visualizations

### **🗺️ Hotspot Intelligence**
- **Question:** *Where are terrorism hotspots emerging over time?*
- Interactive global heatmap with intensity scores
- Threat level classifications (Critical, High, Moderate, Low)
- Trend analysis (Accelerating, Stable, Declining)
- Geographic spread visualization

### **📈 Group Expansion Tracking**
- **Question:** *What groups are expanding their operational reach fastest?*
- Expansion velocity metrics (countries/year)
- Recent expansion trends (5-year window)
- Geographic reach analysis
- Threat classification by expansion rate

### **🌐 Cross-Border Networks**
- **Question:** *Which countries face the most cross-border terrorism spillovers?*
- Interactive network graph linking source and target countries
- Spillover risk index choropleth map
- Source diversity analysis
- Shared group tracking

### **🔮 Predictive Analytics**
- **Question:** *Can we predict where and when the next attack might occur?*
- Time series trend analysis
- Risk scoring based on momentum and volatility
- Feature importance visualization
- High-risk country identification

### **🧬 Behavioral Clustering**
- **Question:** *Are there clusters of groups with similar behavioral patterns?*
- 3D K-means clustering visualization
- Behavioral archetype classification
- Tactical preference heatmaps
- Targeting pattern analysis

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL database running with dbt marts materialized
- dbt models successfully built

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements_dashboard.txt
```

2. **Verify environment variables:**
Ensure your `.env` file contains:
```bash
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=geopolitical_platform
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
```

3. **Ensure dbt models are built:**
```bash
cd dbt_project
dbt run
```

4. **Run the dashboard:**
```bash
streamlit run dashboard.py
```

5. **Access the dashboard:**
Open your browser to `http://localhost:8501`

## 📊 Data Requirements

The dashboard expects the following mart tables to exist in your database:

- `marts.emerging_hotspots` - Hotspot analysis with intensity scores
- `marts.group_expansion` - Group expansion velocity metrics
- `marts.cross_border_risk` - Cross-border spillover risk analysis
- `marts.forecasting_dataset` - Predictive features and time series
- `marts.group_clustering_features` - Behavioral clustering features

These are automatically created when you run `dbt run` on the project.

## 🎨 Dashboard Theme

The dashboard features a dark, FBI/detective-style theme with:
- **Dark blue gradient backgrounds** (#0a0e27 → #1a1f3a)
- **Electric blue accents** (#4a90e2)
- **Courier New monospace font** for that authentic intelligence feel
- **Color-coded threat levels:**
  - 🔴 Critical: Red (#ff0000)
  - 🟠 High: Orange (#ff6600)
  - 🟡 Moderate: Yellow (#ffcc00)
  - 🟢 Low: Green (#00cc00)

## 📈 Visualizations

### Interactive Maps
- **Scatter Mapbox** - Hotspot heatmap with zoom and pan
- **Choropleth** - Spillover risk index by country

### Charts & Graphs
- **3D Scatter Plot** - Behavioral clustering in feature space
- **Network Graph** - Cross-border terrorism flows (using NetworkX)
- **Time Series** - Trend analysis and forecasting
- **Bar Charts** - Rankings and comparisons
- **Heatmaps** - Tactical preference matrices

### Advanced Analytics
- **K-means Clustering** - 5-cluster behavioral segmentation
- **Risk Scoring** - Multi-factor predictive modeling
- **Network Analysis** - Graph-based relationship mapping

## 🔧 Configuration

### Database Connection
The dashboard reads from environment variables. You can also configure connection in the code:

```python
conn = psycopg2.connect(
    host='your_host',
    port=5432,
    database='your_database',
    user='your_user',
    password='your_password'
)
```

### Caching
- Data queries are cached for 5 minutes (300 seconds)
- Clear cache from the Streamlit UI: "☰" menu → "Clear cache"

## 🛠️ Troubleshooting

### Database Connection Issues
```
⚠️ Database Connection Error
```
**Solution:** Verify your database is running and environment variables are set correctly.

```bash
# Test database connection
psql -h localhost -U postgres -d geopolitical_platform
```

### Missing Tables
```
relation "marts.emerging_hotspots" does not exist
```
**Solution:** Run dbt to materialize marts:
```bash
cd dbt_project
dbt run --select marts
```

### Import Errors
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:** Install requirements:
```bash
pip install -r requirements_dashboard.txt
```

## 📱 Performance Tips

1. **Use the sidebar filters** to narrow down data queries
2. **Cache is enabled** - subsequent page loads are fast
3. **Close unused visualizations** by collapsing sections
4. **Refresh data** by clicking "R" or using the clear cache menu

## 🔒 Security Note

This dashboard displays sensitive threat intelligence data. The classification banner indicates:
```
🔒 RESTRICTED - THREAT INTELLIGENCE ANALYSIS 🔒
```

**In production:**
- Add authentication (e.g., `streamlit-authenticator`)
- Use SSL/TLS for database connections
- Implement role-based access control
- Deploy behind a VPN or firewall

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

## 🤝 Contributing

To extend the dashboard:

1. **Add new visualizations** in the respective page sections
2. **Create new pages** by adding to the sidebar radio options
3. **Enhance styling** by modifying the CSS in the `st.markdown()` block
4. **Add filters** using Streamlit widgets (`st.selectbox`, `st.slider`, etc.)

## 📄 License

This dashboard is built on the Global Terrorism Database (GTD). Please review GTD usage terms and cite appropriately.

## 🙏 Acknowledgments

- **Data Source:** Global Terrorism Database (START Consortium)
- **Built with:** Streamlit, Plotly, dbt, PostgreSQL
- **Design Inspiration:** FBI/CIA intelligence dashboards

---

**For questions or issues, please contact your system administrator.**

*Last Updated: 2025*
