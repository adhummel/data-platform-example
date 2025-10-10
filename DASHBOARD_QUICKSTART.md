# 🚀 Dashboard Quick Start Guide

## Launch in 3 Steps

### 1️⃣ Ensure Database is Ready
```bash
cd dbt_project
dbt run --select marts
```

### 2️⃣ Launch Dashboard
```bash
# Option A: Use the launcher script (recommended)
./run_dashboard.sh

# Option B: Manual launch
pip install -r requirements_dashboard.txt
streamlit run dashboard.py
```

### 3️⃣ Open Browser
Navigate to: **http://localhost:8501**

---

## 🎯 What You'll See

### **📊 Executive Dashboard**
- Critical threat metrics at a glance
- Real-time hotspot alerts
- Quick overview charts

### **🗺️ Hotspot Intelligence**
- Interactive global heatmap
- Emerging threat zones
- Intensity scoring

### **📈 Group Expansion Tracking**
- Fastest expanding organizations
- Geographic reach metrics
- Expansion velocity trends

### **🌐 Cross-Border Networks**
- Network graph of terrorism flows
- Spillover risk analysis
- Source-target relationships

### **🔮 Predictive Analytics**
- Risk forecasting
- Temporal trend analysis
- High-risk country identification

### **🧬 Behavioral Clustering**
- 3D group clustering
- Tactical preference analysis
- Behavioral archetypes

---

## 🎨 Dashboard Theme

**FBI/Detective Style:**
- 🌑 Dark blue gradients
- ⚡ Electric blue accents
- 🔤 Monospace fonts
- 🚨 Color-coded threat levels

---

## 🔧 Troubleshooting

### Database connection error?
```bash
# Check if PostgreSQL is running
psql -h localhost -U postgres -d geopolitical_platform

# Verify .env file
cat .env
```

### Missing tables?
```bash
# Re-run dbt models
cd dbt_project
dbt run
```

### Module not found?
```bash
# Reinstall requirements
pip install -r requirements_dashboard.txt
```

---

## 📊 Key Metrics Explained

| Metric | Description |
|--------|-------------|
| **Hotspot Intensity Score** | 0-100 scale measuring threat concentration |
| **Expansion Velocity** | Countries/year expansion rate |
| **Spillover Risk Score** | Cross-border threat index |
| **Threat Level** | Critical → High → Moderate → Low |

---

## 💡 Pro Tips

1. **Use sidebar navigation** to switch between analysis modules
2. **Hover over visualizations** for detailed tooltips
3. **Data refreshes every 5 minutes** (auto-cached)
4. **Export charts** using Plotly's download button (📷)
5. **Filter data** using interactive selections

---

## 🎯 Intelligence Questions Answered

✅ Where are terrorism hotspots emerging over time?
✅ What groups are expanding their operational reach fastest?
✅ Which countries face the most cross-border terrorism spillovers?
✅ Can we predict where and when the next attack might occur?
✅ Are there clusters of groups with similar behavioral patterns?

---

## 📞 Need Help?

Check the full documentation: `DASHBOARD_README.md`

---

**🔒 RESTRICTED - THREAT INTELLIGENCE ANALYSIS 🔒**
