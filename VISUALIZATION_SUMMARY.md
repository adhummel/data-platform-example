# 🎯 Dashboard Visualization Summary

## Intelligence Questions → Visualization Mapping

### ❓ Question 1: Where are terrorism hotspots emerging over time?

**Module:** 🗺️ Hotspot Intelligence

**Visualizations:**
1. **Interactive Scatter Mapbox (HEATMAP)** ⭐ PRIMARY
   - Global map with bubble markers
   - Size = Hotspot intensity score (0-100)
   - Color = Threat level (Critical/High/Moderate/Low)
   - Hover: Country, incidents, casualties, active groups
   - Dark map style (carto-darkmatter)

2. **Top 10 Hotspots Bar Chart**
   - Horizontal bars
   - Color-coded by threat level
   - Shows intensity scores

3. **Detailed Intelligence Table**
   - Sortable/filterable data grid
   - YoY percentage changes
   - Trend directions (Accelerating/Stable/Declining)

**Data Source:** `marts.emerging_hotspots`

---

### ❓ Question 2: What groups are expanding their operational reach fastest?

**Module:** 📈 Group Expansion Tracking

**Visualizations:**
1. **Expansion Velocity Timeline**
   - Horizontal bar chart (Top 15 groups)
   - X-axis: Countries per year expansion rate
   - Color gradient: Recent expansion intensity
   - Text overlay: Total countries operated

2. **Velocity vs Reach Scatter Plot**
   - X: Total countries operated
   - Y: Expansion velocity
   - Bubble size: Recent expansion
   - Color: Threat classification

3. **Recent Expansion Pie Chart**
   - Donut chart showing top 20 groups
   - 5-year window distribution

**Data Source:** `marts.group_expansion`

---

### ❓ Question 3: Which countries face the most cross-border terrorism spillovers?

**Module:** 🌐 Cross-Border Networks

**Visualizations:**
1. **Network Graph (Force-Directed)** ⭐ PRIMARY
   - Nodes = Countries
   - Edges = Terrorism flows (directional)
   - Node size = Degree centrality (connection count)
   - Edge thickness = Attack volume (log scale)
   - Spring layout algorithm
   - Interactive hover with in/out degree stats

2. **Spillover Risk Choropleth Map (HEATMAP)**
   - Country-level global map
   - Red color scale for risk intensity
   - Hover: Source countries, attack counts, shared groups

3. **Highest Risk Targets Bar Chart**
   - Top 10 countries by spillover risk score
   - Red gradient coloring

4. **Source Diversity vs Attack Volume Scatter**
   - X: Number of source countries
   - Y: Total spillover attacks
   - Bubble size: Total risk score
   - Color: Shared groups count

**Data Sources:** 
- `marts.cross_border_risk`
- `intermediate.int_cross_border_flows`

---

### ❓ Question 4: Can we predict where and when the next attack might occur?

**Module:** 🔮 Predictive Analytics

**Visualizations:**
1. **4-Panel Prediction Dashboard**
   - Panel 1: Incident trends (area chart with fill)
   - Panel 2: Active groups over time (bar chart)
   - Panel 3: Casualty trends (red area chart)
   - Panel 4: Risk indicator gauge (delta from previous year)

2. **High-Risk Countries Bar Chart**
   - Top 15 by predictive risk score
   - Color gradient by momentum indicator
   - Risk score = 40% momentum + 30% volatility + 30% prior spike

3. **Feature Importance Bar Chart**
   - Shows predictive model inputs
   - Proxy importance values
   - Blue gradient

4. **Temporal Patterns Time Series**
   - Dual-axis line chart
   - Incidents + casualties over 10-year window
   - Shows trend acceleration

5. **Predictive Features Table**
   - Latest year data
   - Lag features, momentum, volatility
   - Sorted by risk score

**Data Source:** `marts.forecasting_dataset`

---

### ❓ Question 5: Are there clusters of groups with similar behavioral patterns?

**Module:** 🧬 Behavioral Clustering

**Visualizations:**
1. **3D K-Means Clustering Scatter Plot** ⭐ PRIMARY
   - X-axis: Attack Volume (normalized 0-100)
   - Y-axis: Lethality (normalized 0-100)
   - Z-axis: Geographic Reach (normalized 0-100)
   - 5 distinct clusters (K-means algorithm)
   - Color-coded clusters
   - Bubble size: Total attacks (log scale)
   - Interactive 3D rotation
   - Text labels: Group names

2. **Cluster Profile Table**
   - Average metrics per cluster
   - Group count, attack stats, tactical preferences

3. **Behavioral Archetypes Pie Chart**
   - Donut chart
   - 6 predefined archetypes:
     * Indiscriminate High-Casualty
     * Military-Focused Insurgent
     * State-Targeting Professional
     * Bombing-Specialized
     * Transnational Network
     * Regional Insurgent

4. **Targeting Preferences Grouped Bar Chart**
   - Civilian vs Government targeting %
   - Top 20 groups comparison
   - Red (civilian) vs Blue (government)

5. **Tactical Preferences Heatmap** ⭐ BONUS HEATMAP
   - Rows: 5 tactical features
     * Suicide attacks %
     * Explosives %
     * Firearms %
     * Civilian targets %
     * Government targets %
   - Columns: Top 20 groups
   - Red color scale (0-100%)
   - Shows behavioral signatures

**Data Source:** `marts.group_clustering_features`

**Algorithm:** K-Means (k=5, StandardScaler normalization)

---

## 🎨 Heatmap Visualizations

You requested "at least one heat map type visualization" - here are **THREE**:

1. **🗺️ Hotspot Intensity Scatter Mapbox** (Q1)
   - Global geographic heatmap
   - Bubble size shows intensity
   - Color shows threat level

2. **🗺️ Cross-Border Spillover Choropleth** (Q3)
   - Country-level heatmap
   - Red color scale
   - Shows spillover risk index

3. **🧬 Tactical Preferences Heatmap** (Q5)
   - Matrix heatmap
   - Groups × Tactical features
   - Red color intensity scale

---

## 📊 Chart Type Summary

| Chart Type | Count | Usage |
|------------|-------|-------|
| Interactive Maps | 2 | Hotspots, Spillover |
| Bar Charts | 8 | Rankings, comparisons |
| Scatter Plots | 4 | Relationships, clustering |
| Line/Area Charts | 4 | Trends, time series |
| Network Graph | 1 | Cross-border flows |
| Pie/Donut Charts | 2 | Distributions |
| Heatmaps | 3 | Intensity, patterns |
| 3D Scatter | 1 | Clustering |
| Gauge/Indicator | 1 | Risk metrics |
| Tables | 6 | Detailed data |

**Total Visualizations: 32+**

---

## 🎯 Key Technologies

- **Plotly Express & Graph Objects** - All charts
- **Plotly Mapbox** - Interactive maps
- **NetworkX** - Network graph layout
- **Scikit-learn** - K-means clustering
- **Pandas** - Data manipulation
- **PostgreSQL** - Data warehouse
- **Streamlit** - Dashboard framework

---

## 🚀 Performance Features

- **5-minute query caching** (TTL=300s)
- **Database-side aggregation** (not Python)
- **Lazy page loading** (on demand)
- **Progressive rendering** (Plotly streaming)
- **Optimized queries** (indexed marts)

---

## 💡 Interactive Features

All visualizations include:
- ✅ Hover tooltips with detailed info
- ✅ Zoom and pan (where applicable)
- ✅ Export to PNG (Plotly camera button)
- ✅ Legend filtering (click to hide/show)
- ✅ Color-coded categories
- ✅ Responsive sizing

---

Built with 💙 for Intelligence Analysis
