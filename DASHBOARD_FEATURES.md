# 🎯 Dashboard Features Overview

## 🎨 Visual Design

### Theme: FBI/Detective Intelligence Platform
- **Background:** Dark blue gradient (#0a0e27 → #1a1f3a)
- **Accent Color:** Electric blue (#4a90e2)
- **Font:** Courier New (monospace)
- **Style:** High-tech intelligence agency aesthetic

### Classification Banner
```
🔒 RESTRICTED - THREAT INTELLIGENCE ANALYSIS 🔒
```

---

## 📊 Page-by-Page Breakdown

### 1. Executive Dashboard (Landing Page)

**Purpose:** High-level overview for decision-makers

**Widgets:**
- 4 KPI metrics cards:
  - Critical Hotspots count
  - High-Threat Groups count
  - High Spillover Risk countries
  - Total Recent Incidents

**Visualizations:**
- 🚨 Critical Alerts section (red alert boxes)
- 📊 Top 10 Hotspots (horizontal bar chart)
- 📈 Fastest Expanding Groups (horizontal bar chart)

**Intelligence Value:** Instant situational awareness

---

### 2. Hotspot Intelligence 🗺️

**Intelligence Question:**
> "Where are terrorism hotspots emerging over time?"

**Main Visualization:** Interactive Scatter Mapbox
- Global map with circular markers
- Marker size = Intensity score
- Color = Threat level (Red/Orange/Yellow/Green)
- Dark map style for contrast

**Hover Info:**
- Country & region
- Recent incidents
- Casualties
- Active groups
- Hotspot status

**Secondary View:** Detailed intelligence table
- Sortable columns
- YoY change percentages
- Trend direction indicators

**Features:**
- Zoom/pan navigation
- Filter by threat level
- Trend classification

---

### 3. Group Expansion Tracking 📈

**Intelligence Question:**
> "What groups are expanding their operational reach fastest?"

**Main Visualization:** Expansion Timeline
- Horizontal bar chart (top 15 groups)
- X-axis: Expansion velocity (countries/year)
- Color gradient: Recent expansion intensity
- Text labels: Total countries operated

**Secondary Charts:**
1. **Scatter Plot:** Velocity vs Total Reach
   - Bubble size = Recent expansion
   - Color = Threat classification

2. **Pie Chart:** Recent expansion distribution
   - Shows top 20 groups
   - Donut style for modern look

**Data Table:**
- Expansion rank
- Velocity metrics
- Base country
- Threat classification

---

### 4. Cross-Border Networks 🌐

**Intelligence Question:**
> "Which countries face the most cross-border terrorism spillovers?"

**Main Visualization:** Network Graph (Force-directed)
- Nodes = Countries
- Edges = Terrorism flows
- Node size = Connection count
- Edge thickness = Attack volume
- Interactive: Hover for details

**Secondary Visualizations:**

1. **Choropleth Map:** Spillover Risk Index
   - Country-level heatmap
   - Red color scale
   - Global view

2. **Bar Chart:** Highest Risk Targets
   - Top 10 countries
   - Color-coded risk scores

3. **Scatter Plot:** Source Diversity vs Attack Volume
   - Bubble size = Total risk
   - Color = Shared groups

**Network Features:**
- Spring layout algorithm
- Directional edges (source → target)
- Hover shows incoming/outgoing flows

---

### 5. Predictive Analytics 🔮

**Intelligence Question:**
> "Can we predict where and when the next attack might occur?"

**Main Visualization:** 4-Panel Dashboard

**Panel 1:** Incident Trends & Momentum
- Line chart with area fill
- Historical incident counts
- Trend line overlay

**Panel 2:** Active Groups Over Time
- Bar chart by year
- Shows organizational growth

**Panel 3:** Casualty Trends
- Red area chart
- Tracks lethality over time

**Panel 4:** Risk Indicator (Gauge)
- Shows latest year's incidents
- Delta from previous year
- Percentage change

**Secondary Charts:**

1. **Risk Score Bar Chart**
   - Top 15 high-risk countries
   - Color gradient by momentum

2. **Feature Importance**
   - Shows predictive model inputs
   - Blue gradient bars

3. **Temporal Patterns**
   - Dual-axis line chart
   - Incidents + Casualties
   - 10-year window

**Risk Scoring:**
- Momentum (40%)
- Volatility (30%)
- Prior year spike (30%)

---

### 6. Behavioral Clustering 🧬

**Intelligence Question:**
> "Are there clusters of groups with similar behavioral patterns?"

**Main Visualization:** 3D Scatter Plot
- X-axis: Attack Volume (normalized)
- Y-axis: Lethality (normalized)
- Z-axis: Geographic Reach (normalized)
- 5 distinct clusters (K-means)
- Color-coded by cluster
- Bubble size = Total attacks
- Interactive rotation

**Cluster Names:**
- Cluster A: High-Volume Regional
- Cluster B: High-Lethality Extremists
- Cluster C: Transnational Networks
- Cluster D: Tactical Insurgents
- Cluster E: Emerging Threats

**Secondary Visualizations:**

1. **Cluster Profile Table**
   - Average metrics per cluster
   - Group count per cluster

2. **Behavioral Archetypes Pie Chart**
   - Distribution of predefined archetypes
   - Donut style

3. **Targeting Preferences Bar Chart**
   - Grouped bar chart
   - Civilian vs Government targeting
   - Top 20 groups

4. **Tactical Preferences Heatmap**
   - Rows: Tactical features
   - Columns: Top 20 groups
   - Red color scale
   - Features: Suicide attacks, Explosives, Firearms, Targeting

**Machine Learning:**
- K-means clustering (k=5)
- StandardScaler normalization
- 9-feature vector space

---

## 🎛️ Interactive Features

### Global Features (All Pages)
- **Sidebar Navigation:** Radio buttons for page selection
- **Hover Tooltips:** Detailed info on all charts
- **Zoom/Pan:** On maps and network graphs
- **Export:** Download charts as PNG (Plotly button)
- **Data Caching:** 5-minute TTL for performance

### Filters & Controls
- Threat level filtering
- Time window selection
- Group/country search
- Sort by various metrics

---

## 📊 Data Sources

All visualizations pull from dbt marts:
- `marts.emerging_hotspots`
- `marts.group_expansion`
- `marts.cross_border_risk`
- `marts.forecasting_dataset`
- `marts.group_clustering_features`
- `intermediate.int_cross_border_flows`

---

## 🎨 Color Palette

### Threat Levels
```
Critical:  #ff0000 (Red)
High:      #ff6600 (Orange)
Moderate:  #ffcc00 (Yellow)
Low:       #00cc00 (Green)
```

### UI Colors
```
Primary:   #4a90e2 (Electric Blue)
Secondary: #1e3c72 (Navy Blue)
Background: #0a0e27 → #1a1f3a (Gradient)
Text:      #ffffff (White)
Accent:    #a8d0ff (Light Blue)
```

### Chart Color Scales
- **Heatmaps:** Reds (intensity)
- **Clusters:** Blues, Oranges, Reds, Greens, Yellows
- **Trends:** Blue with gradient fill
- **Risk:** Red gradient

---

## 🔢 Key Metrics Displayed

| Metric | Format | Description |
|--------|--------|-------------|
| Hotspot Intensity Score | 0-100 | Composite threat index |
| Expansion Velocity | X.XX countries/year | Speed of geographic spread |
| Spillover Risk Score | 0-1000+ | Cross-border threat index |
| Incidents YoY Change | +/- XX.X% | Year-over-year growth |
| Casualty Count | #,### | Total killed + wounded |
| Active Groups | ### | Distinct organizations |
| Risk Score | 0-100 | Predictive threat score |

---

## 🚀 Performance

### Optimization Features
- **Query caching** (5-minute TTL)
- **Data aggregation** in database (not Python)
- **Lazy loading** (pages load on demand)
- **Efficient queries** (indexed mart tables)
- **Progressive rendering** (Plotly streaming)

### Load Times (typical)
- Executive Dashboard: < 2 seconds
- Hotspot Map: < 3 seconds
- Network Graph: < 4 seconds
- 3D Clustering: < 3 seconds

---

## 📱 Responsive Design

- **Desktop optimized** (primary use case)
- **Wide layout** for dual monitors
- **Collapsible sidebar** for more screen space
- **Full-width charts** adapt to window size
- **Mobile accessible** (basic functionality)

---

## 🎯 User Experience

### Navigation Flow
1. Land on **Executive Dashboard** for overview
2. Dive into specific modules via **sidebar**
3. Interact with **visualizations** for detail
4. Review **data tables** for exact values
5. Export **charts** for reports

### Information Hierarchy
1. **Classification Banner** (always visible)
2. **Page Title** with intelligence question
3. **Main Visualization** (hero section)
4. **Supporting Charts** (2-column layout)
5. **Detailed Tables** (bottom section)

---

## 🔧 Customization Points

Want to modify the dashboard? Here's where to look:

### Change Colors
- Line 24-126 in `dashboard.py` (CSS section)

### Add New Page
- Line 569-586 (sidebar navigation)
- Create new elif block for your page

### Modify Visualizations
- Each `create_*()` function is self-contained
- Edit Plotly figure objects directly

### Adjust Data Queries
- Modify SQL in `load_*()` functions
- Add WHERE clauses for filtering

### Theme Tweaks
- Update `color_discrete_map` in each viz
- Modify `update_layout()` calls

---

## 💡 Best Practices

### For Analysts
1. Start with **Executive Dashboard**
2. Note **critical alerts** (red boxes)
3. Deep-dive into relevant modules
4. Cross-reference multiple views
5. Export visuals for briefings

### For Presentations
1. Use **full-screen mode** (F11)
2. Hide **sidebar** (☰ → collapse)
3. Hover for **detailed tooltips**
4. Use **download button** for screenshots
5. Rehearse **page transitions**

### For Developers
1. Check **data refresh** before demos
2. Test **database connection** first
3. Clear **cache** if data updated
4. Monitor **query performance**
5. Review **error logs** for issues

---

**Built with 💙 for Intelligence Professionals**
