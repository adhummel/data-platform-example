# app.py
# Global Threat Intelligence Dashboard (Light Mode, Tab-Based, Postgres-Backed)

import os
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import networkx as nx
import streamlit as st

# --------------------------------------
# Bootstrap
# --------------------------------------
load_dotenv()

st.set_page_config(
    page_title="Global Threat Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------
# Light UI Styles (minimal, professional)
# --------------------------------------
st.markdown("""
<style>
:root {
  --bg: #ffffff;
  --text: #1f2937;         /* gray-800 */
  --muted: #4b5563;        /* gray-600 */
  --border: #e5e7eb;       /* gray-200 */
  --card: #ffffff;
  --accent: #2563eb;       /* blue-600 */
}
html, body, [class*="css"] { font-family: "Helvetica Neue", Inter, system-ui, -apple-system, Segoe UI, Arial, sans-serif; }
h1,h2,h3,h4,h5 { color: var(--text); font-weight: 650; }
p, li, label { color: var(--muted); }

.header { margin-bottom: 0.75rem; }
.title { font-size: 2.0rem; font-weight: 700; color: #111827; }
.subtitle { font-size: 0.95rem; color: #6b7280; margin-top: 0.25rem; }

.section { margin-top: 1.5rem; }

.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1.0rem 1.2rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.06);
}

.metric .label { font-size: 0.85rem; color: #6b7280; }
.metric .value { font-size: 1.5rem; font-weight: 650; color: #111827; }

footer { color:#9ca3af; font-size:0.8rem; text-align:center; margin-top:2rem; }
</style>
""", unsafe_allow_html=True)

# --------------------------------------
# Header
# --------------------------------------
st.markdown(
    f"""
<div class="header">
  <div class="title">Global Threat Intelligence Dashboard</div>
  <div class="subtitle">Data-driven insights into hotspots, group expansion, cross-border spillovers, and predictive indicators</div>
</div>
""",
    unsafe_allow_html=True
)

# --------------------------------------
# Database utils
# --------------------------------------
@st.cache_resource
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DATABASE_HOST", "localhost"),
        port=int(os.getenv("DATABASE_PORT", 5432)),
        database=os.getenv("DATABASE_NAME", "geopolitical_platform"),
        user=os.getenv("DATABASE_USER", "postgres"),
        password=os.getenv("DATABASE_PASSWORD", "postgres"),
        cursor_factory=RealDictCursor,
    )

@st.cache_data(ttl=600, show_spinner=False)
def run_query(sql: str, params: tuple = None) -> pd.DataFrame:
    conn = get_db_connection()
    df = pd.read_sql_query(sql, conn, params=params)
    return df

# --------------------------------------
# Data loaders (dbt outputs expected)
# --------------------------------------
def load_hotspots():
    q = """
      SELECT * 
      FROM dbt_marts.emerging_hotspots
      ORDER BY hotspot_intensity_score DESC
    """
    return run_query(q)

def load_group_expansion():
    q = """
      SELECT *
      FROM dbt_marts.group_expansion
      ORDER BY expansion_velocity DESC
      LIMIT 100
    """
    return run_query(q)

def load_cross_border():
    q = """
      SELECT *
      FROM dbt_marts.cross_border_risk
      ORDER BY total_spillover_risk_score DESC
      LIMIT 200
    """
    return run_query(q)

def load_forecasting():
    q = """
      SELECT *
      FROM dbt_marts.forecasting_dataset
      ORDER BY year DESC, country
      LIMIT 2000
    """
    return run_query(q)

def load_clustering():
    q = """
      SELECT *
      FROM dbt_marts.group_clustering_features
      ORDER BY total_attacks DESC
      LIMIT 300
    """
    return run_query(q)

def load_network_edges():
    q = """
      SELECT DISTINCT
          cf.source_country,
          cf.target_country,
          cf.total_spillover_attacks as weight,
          cf.num_shared_groups,
          cf.spillover_intensity_score
      FROM dbt_intermediate.int_cross_border_flows cf
      WHERE cf.total_spillover_attacks > 5
      ORDER BY cf.spillover_intensity_score DESC
      LIMIT 300
    """
    return run_query(q)

# --------------------------------------
# Visualization helpers (light theme)
# --------------------------------------
PLOT_TEMPLATE = "simple_white"

def fig_area(x, y, title):
    fig = px.area(x=x, y=y, title=title, template=PLOT_TEMPLATE)
    fig.update_traces(line_color="#2563eb", fillcolor="rgba(37,99,235,0.15)")
    fig.update_layout(height=380, margin=dict(l=16, r=16, t=56, b=16))
    return fig

def hotspot_geo_scatter(df):
    fig = px.scatter_geo(
        df,
        lat="latitude",
        lon="longitude",
        color="threat_level",
        size="hotspot_intensity_score",
        hover_name="country",
        projection="natural earth",
        color_discrete_map={
            "Critical": "#dc2626",
            "High": "#f97316",
            "Moderate": "#eab308",
            "Low": "#16a34a",
        },
        template=PLOT_TEMPLATE,
        title="Global Terrorism Hotspot Intensity Map",
    )
    fig.update_layout(height=480, margin=dict(l=0, r=0, t=56, b=0))
    return fig

def expansion_bar(df):
    fig = px.bar(
        df.sort_values("expansion_velocity"),
        x="expansion_velocity",
        y="primary_group",
        orientation="h",
        color="expansion_velocity",
        color_continuous_scale="Blues",
        template=PLOT_TEMPLATE,
        title="Fastest Expanding Organizations",
    )
    fig.update_layout(height=460, coloraxis_showscale=False, margin=dict(l=16, r=16, t=56, b=16))
    return fig

def spillover_choropleth(df):
    fig = px.choropleth(
        df,
        locations="target_country",
        locationmode="country names",
        color="total_spillover_risk_score",
        hover_name="target_country",
        hover_data={
            "num_source_countries": True,
            "total_spillover_attacks": True,
            "total_shared_groups": True,
            "target_country": False,
        },
        color_continuous_scale="Reds",
        template=PLOT_TEMPLATE,
        title="Cross-Border Terrorism Spillover Risk Index",
    )
    fig.update_layout(height=520, margin=dict(l=0, r=0, t=56, b=0))
    return fig

def network_graph(edges_df):
    # Build graph
    G = nx.DiGraph()
    for _, row in edges_df.iterrows():
        G.add_edge(
            row["source_country"],
            row["target_country"],
            weight=row["weight"],
            groups=row["num_shared_groups"],
            intensity=row["spillover_intensity_score"],
        )

    if len(G.nodes) == 0:
        return go.Figure().update_layout(title="No edges to display.")

    pos = nx.spring_layout(G, k=1.6, iterations=60, seed=42)

    edge_traces = []
    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        width = max(1.0, float(np.log1p(data["weight"]) * 0.9))
        edge_traces.append(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode="lines",
                line=dict(width=width, color="rgba(37,99,235,0.30)"),
                hoverinfo="none",
                showlegend=False,
            )
        )

    node_x, node_y, node_text, node_size = [], [], [], []
    for n in G.nodes():
        x, y = pos[n]
        node_x.append(x)
        node_y.append(y)
        deg = G.degree(n)
        node_size.append(8 + deg * 2)
        node_text.append(f"{n} • deg={deg}")

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode="markers+text",
        text=[str(t)[:20] for t in G.nodes()],
        textposition="top center",
        textfont=dict(size=9),
        hovertext=node_text,
        hovertemplate="%{hovertext}<extra></extra>",
        marker=dict(size=node_size, color="#2563eb", line=dict(width=1, color="#ffffff")),
        showlegend=False,
    )

    fig = go.Figure(data=edge_traces + [node_trace])
    fig.update_layout(
        title="Cross-Border Terrorism Network",
        height=560,
        margin=dict(l=16, r=16, t=56, b=16),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        template=PLOT_TEMPLATE,
    )
    return fig

def clustering_3d(df):
    # Features expected from your dbt_marts.group_clustering_features
    features = [
        "normalized_attack_volume",
        "normalized_lethality",
        "normalized_geographic_reach",
        "suicide_attack_rate_pct",
        "success_rate_pct",
        "explosives_pct",
        "firearms_pct",
        "govt_target_pct",
        "civilian_target_pct",
    ]
    X = df[features].fillna(0.0).astype(float)

    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)

    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    df = df.copy()
    df["cluster"] = kmeans.fit_predict(Xs)

    fig = go.Figure()
    palette = ["#2563eb", "#f97316", "#dc2626", "#16a34a", "#eab308"]

    for c in sorted(df["cluster"].unique()):
        part = df[df["cluster"] == c]
        fig.add_trace(go.Scatter3d(
            x=part["normalized_attack_volume"],
            y=part["normalized_lethality"],
            z=part["normalized_geographic_reach"],
            mode="markers",
            name=f"Cluster {c}",
            marker=dict(
                size=np.clip(np.log1p(part["total_attacks"]), 4, 16),
                color=palette[c % len(palette)],
                opacity=0.85,
                line=dict(width=0.5, color="#ffffff")
            ),
            text=part["primary_group"],
            hovertemplate="<b>%{text}</b><br>Vol: %{x:.2f} • Leth: %{y:.2f} • Reach: %{z:.2f}<extra></extra>"
        ))

    fig.update_layout(
        title="Behavioral Clustering (3D): Volume × Lethality × Reach",
        scene=dict(
            xaxis_title="Attack Volume (norm.)",
            yaxis_title="Lethality (norm.)",
            zaxis_title="Geographic Reach (norm.)",
        ),
        height=560,
        template=PLOT_TEMPLATE,
        margin=dict(l=16, r=16, t=56, b=16),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig, df

# --------------------------------------
# Data Fetch (fail fast if DB down)
# --------------------------------------
try:
    hotspots_df = load_hotspots()
    groups_df = load_group_expansion()
    spillover_df = load_cross_border()
    forecast_df = load_forecasting()
    cluster_df = load_clustering()
    network_df = load_network_edges()
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.info("Verify environment variables and that PostgreSQL is reachable.")
    st.code("""# Required environment variables
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=geopolitical_platform
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
""")
    st.stop()

# --------------------------------------
# Tabs (top, horizontal)
# --------------------------------------
tab_exec, tab_hotspots, tab_groups, tab_cross, tab_predict, tab_cluster = st.tabs([
    "Executive Summary",
    "Hotspot Intelligence",
    "Group Expansion",
    "Cross-Border Networks",
    "Predictive Analytics",
    "Behavioral Clustering",
])

# --------------------------------------
# Executive Summary
# --------------------------------------
with tab_exec:
    st.markdown("### Executive Summary")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="card metric"><div class="label">Critical Hotspots</div><div class="value">{}</div></div>'.format((hotspots_df["threat_level"]=="Critical").sum()), unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card metric"><div class="label">High-Threat Groups</div><div class="value">{}</div></div>'.format((groups_df["threat_classification"]=="Critical").sum()), unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card metric"><div class="label">Recent Incidents</div><div class="value">{:,.0f}</div></div>'.format(float(hotspots_df["incidents_recent"].sum())), unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="card metric"><div class="label">Active Countries</div><div class="value">{}</div></div>'.format(hotspots_df["country"].nunique()), unsafe_allow_html=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    # Incident Trends over time
    trend = forecast_df.groupby("year", as_index=False).agg(incidents=("incidents_lag1", "sum"))
    st.plotly_chart(fig_area(trend["year"], trend["incidents"], "Global Incident Trend Over Time"), use_container_width=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    # Top Hotspots & Fastest Expanding Groups
    c5, c6 = st.columns(2)
    with c5:
        st.markdown("#### Top Hotspots")
        top_hotspots = hotspots_df.head(12)
        fig = px.bar(
            top_hotspots.sort_values("hotspot_intensity_score"),
            x="hotspot_intensity_score",
            y="country",
            color="threat_level",
            orientation="h",
            color_discrete_map={"Critical":"#dc2626","High":"#f97316","Moderate":"#eab308","Low":"#16a34a"},
            template=PLOT_TEMPLATE
        )
        fig.update_layout(height=420, margin=dict(l=16,r=16,t=40,b=16))
        st.plotly_chart(fig, use_container_width=True)

    with c6:
        st.markdown("#### Fastest Expanding Groups")
        st.plotly_chart(expansion_bar(groups_df.head(15)), use_container_width=True)

# --------------------------------------
# Hotspot Intelligence
# --------------------------------------
with tab_hotspots:
    st.markdown("### Hotspot Intelligence")
    st.markdown("Identify where threat concentrations are emerging and intensifying.")

    st.plotly_chart(hotspot_geo_scatter(hotspots_df), use_container_width=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    st.markdown("#### Detailed Hotspot Table")
    df_display = hotspots_df[[
        "country", "region", "hotspot_status", "threat_level",
        "hotspot_intensity_score", "incidents_recent", "casualties_recent",
        "num_active_groups", "trend_direction", "incidents_yoy_pct_change"
    ]].copy()
    if "incidents_yoy_pct_change" in df_display.columns:
        df_display["incidents_yoy_pct_change"] = df_display["incidents_yoy_pct_change"].apply(
            lambda x: f"{x:.1f}%" if pd.notnull(x) else "—"
        )
    st.dataframe(df_display, use_container_width=True, height=420)

# --------------------------------------
# Group Expansion
# --------------------------------------
with tab_groups:
    st.markdown("### Group Expansion")
    st.markdown("Which organizations are expanding operational reach the fastest?")

    st.plotly_chart(expansion_bar(groups_df.head(20)), use_container_width=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Expansion Velocity vs Total Reach")
        fig = px.scatter(
            groups_df.head(50),
            x="countries_operated",
            y="expansion_velocity",
            size="recent_expansion",
            color="threat_classification",
            hover_name="primary_group",
            labels={"countries_operated":"Total Countries","expansion_velocity":"Velocity (countries/yr)"},
            color_discrete_map={"Critical":"#dc2626","High":"#f97316","Moderate":"#eab308"},
            template=PLOT_TEMPLATE,
        )
        fig.update_layout(height=440, margin=dict(l=16,r=16,t=56,b=16))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Recent Expansion Distribution (Top 20)")
        fig = px.pie(
            groups_df.head(20),
            values="recent_expansion",
            names="primary_group",
            hole=0.45,
            template=PLOT_TEMPLATE
        )
        fig.update_layout(height=440, margin=dict(l=16,r=16,t=56,b=16))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Group Expansion Details")
    st.dataframe(
        groups_df[[
            "primary_group","expansion_rank","expansion_velocity","countries_operated",
            "recent_expansion","years_active","primary_base_country","expansion_rate",
            "threat_classification"
        ]].copy(),
        use_container_width=True,
        height=420
    )

# --------------------------------------
# Cross-Border Networks
# --------------------------------------
with tab_cross:
    st.markdown("### Cross-Border Networks")
    st.markdown("Assess spillover risks and cross-border attack dynamics.")

    st.markdown("#### Terrorism Flow Network")
    st.plotly_chart(network_graph(network_df), use_container_width=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    st.markdown("#### Spillover Risk Map")
    st.plotly_chart(spillover_choropleth(spillover_df), use_container_width=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Highest Risk Targets")
        top_targets = spillover_df.head(12)
        fig = px.bar(
            top_targets.sort_values("total_spillover_risk_score"),
            x="total_spillover_risk_score",
            y="target_country",
            color="total_spillover_risk_score",
            color_continuous_scale="Reds",
            template=PLOT_TEMPLATE,
            orientation="h"
        )
        fig.update_layout(height=420, margin=dict(l=16,r=16,t=56,b=16), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("#### Source Diversity vs Attack Volume")
        take = spillover_df.head(50)
        fig = px.scatter(
            take,
            x="num_source_countries",
            y="total_spillover_attacks",
            size="total_spillover_risk_score",
            color="total_shared_groups",
            hover_name="target_country",
            template=PLOT_TEMPLATE,
        )
        fig.update_layout(height=420, margin=dict(l=16,r=16,t=56,b=16))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("#### Cross-Border Intelligence Table")
    st.dataframe(
        spillover_df[[
            "target_country","num_source_countries","total_spillover_attacks",
            "total_shared_groups","avg_time_to_spillover_years",
            "total_spillover_risk_score","top_source_countries"
        ]].copy(),
        use_container_width=True,
        height=420
    )

# --------------------------------------
# Predictive Analytics
# --------------------------------------
with tab_predict:
    st.markdown("### Predictive Analytics")
    st.markdown("Momentum, volatility, and forward-looking incident indicators.")

    # Time series summary
    yearly = forecast_df.groupby("year", as_index=False).agg({
        "target_incidents_next_year": "sum",
        "incidents_lag1": "sum",
        "casualties_lag1": "sum",
    })
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=yearly["year"], y=yearly["incidents_lag1"],
        mode="lines+markers", name="Historical Incidents",
        line=dict(color="#2563eb", width=3)
    ))
    fig.add_trace(go.Scatter(
        x=yearly["year"], y=yearly["casualties_lag1"] / 10.0,
        mode="lines+markers", name="Casualties (÷10)",
        line=dict(color="#dc2626", width=2), yaxis="y2"
    ))
    fig.update_layout(
        title="Global Terrorism Trends Over Time",
        xaxis_title="Year",
        yaxis_title="Incidents",
        yaxis2=dict(title="Casualties (÷10)", overlaying="y", side="right"),
        template=PLOT_TEMPLATE, height=420, hovermode="x unified",
        margin=dict(l=16, r=16, t=56, b=16)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    # Latest-year risk scatter
    latest_year = int(forecast_df["year"].max())
    latest = forecast_df[forecast_df["year"] == latest_year].copy()
    if not latest.empty:
        st.markdown(f"#### Risk Momentum vs Volatility ({latest_year})")
        risk_fig = px.scatter(
            latest,
            x="incidents_momentum",
            y="incidents_volatility",
            size="target_incidents_next_year",
            color="region",
            hover_name="country",
            template=PLOT_TEMPLATE,
            title=None
        )
        risk_fig.update_layout(height=460, margin=dict(l=16,r=16,t=16,b=16))
        st.plotly_chart(risk_fig, use_container_width=True)

        # Simple composite risk score (weights can match your model)
        if {"incidents_momentum","incidents_volatility","prior_year_spike"}.issubset(latest.columns):
            latest["risk_score"] = (
                latest["incidents_momentum"] * 0.4
                + latest["incidents_volatility"] * 0.3
                + latest["prior_year_spike"] * 0.3
            )
            st.markdown("#### Highest Predicted Risk (Top 15)")
            top_risk = latest.nlargest(15, "risk_score")[[
                "country","region","risk_score","incidents_momentum","incidents_volatility","active_groups","target_incidents_next_year"
            ]].copy()
            st.dataframe(top_risk.reset_index(drop=True).round(3), use_container_width=True, height=420)

# --------------------------------------
# Behavioral Clustering
# --------------------------------------
with tab_cluster:
    st.markdown("### Behavioral Clustering")
    st.markdown("Unsupervised grouping of organizations by tactics, lethality, and reach.")

    fig3d, clustered = clustering_3d(cluster_df)
    st.plotly_chart(fig3d, use_container_width=True)

    st.markdown('<div class="section"></div>', unsafe_allow_html=True)

    # Cluster profiles
    cols_to_mean = [
        "total_attacks",
        "suicide_attack_rate_pct",
        "success_rate_pct",
        "explosives_pct",
        "firearms_pct",
        "civilian_target_pct",
        "govt_target_pct",
        "countries_operated",
    ]
    prof = clustered.groupby("cluster").agg({
        "primary_group": "count",
        **{c: "mean" for c in cols_to_mean}
    }).rename(columns={"primary_group": "group_count"}).reset_index()
    st.markdown("#### Cluster Profiles")
    st.dataframe(prof.round(2), use_container_width=True, height=360)

    # Targeting preferences bar (top 20 by total_attacks)
    st.markdown("#### Targeting Preferences (Top 20 groups)")
    top20 = clustered.sort_values("total_attacks", ascending=False).head(20)
    melted = top20[["primary_group","civilian_target_pct","govt_target_pct"]].melt(
        id_vars="primary_group", var_name="Target Type", value_name="Percentage"
    )
    fig_bar = px.bar(
        melted,
        x="Percentage",
        y="primary_group",
        color="Target Type",
        orientation="h",
        template=PLOT_TEMPLATE
    )
    fig_bar.update_layout(height=460, margin=dict(l=16,r=16,t=56,b=16))
    st.plotly_chart(fig_bar, use_container_width=True)

# --------------------------------------
# Footer
# --------------------------------------
st.markdown(f"<footer>Updated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</footer>", unsafe_allow_html=True)
