import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="Global Threat Analytics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Global Style
# -----------------------------
st.markdown("""
<style>
/* Reset */
*, *::before, *::after {box-sizing: border-box;}
html, body, [class*="css"] {font-family: "Helvetica Neue", Helvetica, Arial, sans-serif; color:#1f2937;}
h1,h2,h3,h4 {font-weight:600; color:#111827;}
p {color:#4b5563;}

/* Layout */
.main-title {
    font-size:2.1rem; font-weight:700; color:#111827;
    margin-bottom:0.25rem;
}
.subtitle {
    font-size:0.95rem; color:#6b7280; margin-bottom:1.5rem;
}
.card {
    background-color:#ffffff;
    border:1px solid #e5e7eb;
    border-radius:10px;
    padding:1.5rem;
    box-shadow:0 1px 3px rgba(0,0,0,0.05);
}
.section {
    margin-top:2.5rem;
}
.metric-label {
    font-size:0.9rem;
    color:#6b7280;
}
.metric-value {
    font-size:1.6rem;
    font-weight:600;
    color:#111827;
}
footer {
    color:#9ca3af; font-size:0.8rem; text-align:center; margin-top:3rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.markdown(f"""
<div>
  <div class="main-title">Global Threat Intelligence Dashboard</div>
  <div class="subtitle">Data-driven insights into geopolitical violence, group expansion, and spillover dynamics</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# Database Connection (cache)
# -----------------------------
@st.cache_resource
def get_db():
    return psycopg2.connect(
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=os.getenv("DATABASE_PORT", 5432),
        database=os.getenv("DATABASE_NAME", "geopolitical_platform"),
        user=os.getenv("DATABASE_USER", "postgres"),
        password=os.getenv("DATABASE_PASSWORD", "postgres")
    )

@st.cache_data(ttl=600)
def run_query(q):
    conn = get_db()
    df = pd.read_sql(q, conn)
    conn.close()
    return df

# -----------------------------
# Load Example Data
# -----------------------------
try:
    hotspots = run_query("SELECT * FROM dbt_marts.emerging_hotspots ORDER BY hotspot_intensity_score DESC LIMIT 50;")
    groups = run_query("SELECT * FROM dbt_marts.group_expansion ORDER BY expansion_velocity DESC LIMIT 30;")
    forecast = run_query("SELECT * FROM dbt_marts.forecasting_dataset ORDER BY year DESC, country LIMIT 500;")
except Exception as e:
    st.error("Database connection failed.")
    st.stop()

# -----------------------------
# Executive Summary
# -----------------------------
st.markdown("### Executive Summary")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-label">Critical Hotspots</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{(hotspots.threat_level=="Critical").sum()}</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-label">High-Threat Groups</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{(groups.threat_classification=="Critical").sum()}</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-label">Total Incidents (Recent)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{hotspots.incidents_recent.sum():,.0f}</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-label">Active Countries</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="metric-value">{hotspots.country.nunique()}</div>', unsafe_allow_html=True)

# -----------------------------
# Incident Trends
# -----------------------------
st.markdown("### Incident Trends")
trend_df = forecast.groupby("year", as_index=False).agg({"incidents_lag1":"sum"})
fig = px.area(trend_df, x="year", y="incidents_lag1",
              title="Global Incident Trend Over Time",
              template="simple_white")
fig.update_traces(line_color="#2563eb", fillcolor="rgba(37,99,235,0.15)")
fig.update_layout(height=400, margin=dict(l=20,r=20,t=60,b=20))
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Regional Hotspots
# -----------------------------
st.markdown("### Regional Hotspots")
hotspot_fig = px.scatter_geo(
    hotspots,
    lat="latitude", lon="longitude",
    color="threat_level",
    size="hotspot_intensity_score",
    hover_name="country",
    projection="natural earth",
    color_discrete_map={
        "Critical":"#dc2626","High":"#f97316","Moderate":"#eab308","Low":"#16a34a"
    },
    template="simple_white",
)
hotspot_fig.update_layout(height=500, margin=dict(l=0,r=0,t=40,b=0))
st.plotly_chart(hotspot_fig, use_container_width=True)

# -----------------------------
# Group Expansion Overview
# -----------------------------
st.markdown("### Expanding Organizations")
top_groups = groups.head(15)
expansion_fig = px.bar(
    top_groups.sort_values("expansion_velocity"),
    x="expansion_velocity", y="primary_group",
    orientation="h", color="expansion_velocity",
    color_continuous_scale="Blues",
    title="Top 15 Fastest Expanding Groups"
)
expansion_fig.update_layout(height=450, template="simple_white", coloraxis_showscale=False)
st.plotly_chart(expansion_fig, use_container_width=True)

# -----------------------------
# Forecast Overview
# -----------------------------
st.markdown("### Predictive Indicators")
latest_year = forecast["year"].max()
latest_data = forecast[forecast["year"] == latest_year]
forecast_fig = px.scatter(
    latest_data,
    x="incidents_momentum",
    y="incidents_volatility",
    size="target_incidents_next_year",
    color="region",
    hover_name="country",
    title=f"Risk Momentum vs Volatility ({latest_year})",
    template="simple_white"
)
forecast_fig.update_layout(height=500)
st.plotly_chart(forecast_fig, use_container_width=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown(f"<footer>Updated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</footer>", unsafe_allow_html=True)
