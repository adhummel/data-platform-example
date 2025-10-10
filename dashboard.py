"""
GEOPOLITICAL THREAT INTELLIGENCE DASHBOARD
FBI-Style Analytics Platform for Global Terrorism Analysis
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import networkx as nx

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="GTD Threat Intelligence Dashboard",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for FBI/Detective Theme
st.markdown("""
<style>
    /* Dark theme with blue accents */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #4a90e2;
        box-shadow: 0 4px 15px rgba(74, 144, 226, 0.3);
        margin-bottom: 30px;
        text-align: center;
    }

    .main-header h1 {
        color: #ffffff;
        font-family: 'Courier New', monospace;
        font-size: 2.5em;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 0 0 10px rgba(74, 144, 226, 0.8);
    }

    .main-header p {
        color: #a8d0ff;
        font-family: 'Courier New', monospace;
        font-size: 1.1em;
        margin: 5px 0 0 0;
    }

    /* Classification banner */
    .classification {
        background: #8b0000;
        color: white;
        text-align: center;
        padding: 5px;
        font-weight: bold;
        font-family: 'Courier New', monospace;
        letter-spacing: 5px;
        margin-bottom: 10px;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #4a90e2;
        box-shadow: 0 2px 10px rgba(74, 144, 226, 0.2);
        margin: 10px 0;
    }

    /* Alerts */
    .alert-critical {
        background: rgba(220, 53, 69, 0.2);
        border: 2px solid #dc3545;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }

    .alert-warning {
        background: rgba(255, 193, 7, 0.2);
        border: 2px solid #ffc107;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }

    /* Data labels */
    .data-label {
        color: #4a90e2;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        font-size: 0.9em;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: #0a0e27;
    }

    /* Section headers */
    .section-header {
        color: #4a90e2;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        font-size: 1.5em;
        border-bottom: 2px solid #4a90e2;
        padding-bottom: 10px;
        margin: 20px 0;
        letter-spacing: 2px;
    }

    /* Status indicators */
    .status-critical { color: #ff4444; font-weight: bold; }
    .status-high { color: #ff9800; font-weight: bold; }
    .status-moderate { color: #ffeb3b; font-weight: bold; }
    .status-low { color: #4caf50; font-weight: bold; }

    /* Timestamp */
    .timestamp {
        color: #6c757d;
        font-family: 'Courier New', monospace;
        font-size: 0.85em;
    }
</style>
""", unsafe_allow_html=True)

# Database connection
@st.cache_resource
def get_db_connection():
    """Establish database connection"""
    return psycopg2.connect(
        host=os.getenv('DATABASE_HOST', 'localhost'),
        port=os.getenv('DATABASE_PORT', 5432),
        database=os.getenv('DATABASE_NAME', 'geopolitical_platform'),
        user=os.getenv('DATABASE_USER', 'postgres'),
        password=os.getenv('DATABASE_PASSWORD', 'postgres')
    )

@st.cache_data(ttl=300)
def load_data(query, _conn):
    """Load data from database with caching"""
    return pd.read_sql(query, _conn)

# Data loading functions
def load_hotspots(conn):
    """Load emerging hotspots data"""
    query = "SELECT * FROM dbt_marts.emerging_hotspots ORDER BY hotspot_intensity_score DESC"
    return load_data(query, conn)

def load_group_expansion(conn):
    """Load group expansion data"""
    query = "SELECT * FROM dbt_marts.group_expansion ORDER BY expansion_velocity DESC LIMIT 50"
    return load_data(query, conn)

def load_cross_border(conn):
    """Load cross-border risk data"""
    query = "SELECT * FROM dbt_marts.cross_border_risk ORDER BY total_spillover_risk_score DESC LIMIT 30"
    return load_data(query, conn)

def load_forecasting(conn):
    """Load forecasting dataset"""
    query = """
        SELECT * FROM dbt_marts.forecasting_dataset
        WHERE year >= (SELECT MAX(year) - 10 FROM dbt_marts.forecasting_dataset)
        ORDER BY year DESC, country
    """
    return load_data(query, conn)

def load_clustering(conn):
    """Load group clustering features"""
    query = "SELECT * FROM dbt_marts.group_clustering_features ORDER BY total_attacks DESC LIMIT 100"
    return load_data(query, conn)

def load_network_data(conn):
    """Load data for network graph"""
    query = """
        SELECT DISTINCT
            cf.source_country,
            cf.target_country,
            cf.total_spillover_attacks as weight,
            cf.num_shared_groups,
            cf.spillover_intensity_score
        FROM intermediate.int_cross_border_flows cf
        WHERE cf.total_spillover_attacks > 5
        ORDER BY cf.spillover_intensity_score DESC
        LIMIT 100
    """
    return load_data(query, conn)

# Visualization functions
def create_hotspot_heatmap(df):
    """Create interactive heatmap of terrorism hotspots"""
    fig = px.scatter_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        size='hotspot_intensity_score',
        color='threat_level',
        hover_name='country',
        hover_data={
            'region': True,
            'incidents_recent': True,
            'casualties_recent': True,
            'num_active_groups': True,
            'hotspot_status': True,
            'latitude': False,
            'longitude': False,
            'hotspot_intensity_score': ':.1f'
        },
        color_discrete_map={
            'Critical': '#ff0000',
            'High': '#ff6600',
            'Moderate': '#ffcc00',
            'Low': '#00cc00'
        },
        size_max=50,
        zoom=1,
        title="Global Terrorism Hotspot Intensity Map"
    )

    fig.update_layout(
        mapbox_style="carto-darkmatter",
        height=700,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Courier New'),
        title_font_size=20,
        title_font_color='#4a90e2',
        margin=dict(l=0, r=0, t=50, b=0)
    )

    return fig

def create_expansion_timeline(df):
    """Create timeline showing group expansion velocity"""
    fig = go.Figure()

    # Get top 15 groups
    top_groups = df.nsmallest(15, 'expansion_rank')

    fig.add_trace(go.Bar(
        x=top_groups['expansion_velocity'],
        y=top_groups['primary_group'],
        orientation='h',
        marker=dict(
            color=top_groups['recent_expansion'],
            colorscale='Reds',
            showscale=True,
            colorbar=dict(title="Recent<br>Expansion", titlefont=dict(color='#ffffff'), tickfont=dict(color='#ffffff'))
        ),
        text=top_groups['countries_operated'],
        texttemplate='%{text} countries',
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Expansion Velocity: %{x:.2f} countries/year<br>Total Countries: %{text}<br><extra></extra>'
    ))

    fig.update_layout(
        title="Fastest Expanding Terrorist Organizations",
        xaxis_title="Expansion Velocity (Countries/Year)",
        yaxis_title="",
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(20,30,50,0.3)',
        font=dict(color='#ffffff', family='Courier New'),
        title_font_color='#4a90e2',
        showlegend=False,
        xaxis=dict(gridcolor='rgba(74, 144, 226, 0.2)'),
        yaxis=dict(gridcolor='rgba(74, 144, 226, 0.2)')
    )

    return fig

def create_network_graph(df):
    """Create network graph of cross-border terrorism flows"""
    # Create networkx graph
    G = nx.DiGraph()

    # Add edges with weights
    for _, row in df.iterrows():
        G.add_edge(
            row['source_country'],
            row['target_country'],
            weight=row['weight'],
            groups=row['num_shared_groups'],
            intensity=row['spillover_intensity_score']
        )

    # Calculate layout
    pos = nx.spring_layout(G, k=2, iterations=50, seed=42)

    # Create edge traces
    edge_trace = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]

        # Edge thickness based on weight
        width = np.log1p(edge[2]['weight']) * 0.5

        edge_trace.append(
            go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=width, color='rgba(74, 144, 226, 0.4)'),
                hoverinfo='none',
                showlegend=False
            )
        )

    # Create node trace
    node_x = []
    node_y = []
    node_text = []
    node_size = []

    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

        # Node size based on degree
        degree = G.degree(node)
        node_size.append(10 + degree * 3)

        # Hover text
        in_degree = G.in_degree(node)
        out_degree = G.out_degree(node)
        node_text.append(f"<b>{node}</b><br>Incoming: {in_degree}<br>Outgoing: {out_degree}")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        hovertemplate='%{text}<extra></extra>',
        text=[node.split('(')[0][:15] for node in G.nodes()],
        textposition='top center',
        textfont=dict(size=9, color='#ffffff'),
        hovertext=node_text,
        marker=dict(
            size=node_size,
            color='#4a90e2',
            line=dict(width=2, color='#ffffff')
        ),
        showlegend=False
    )

    # Create figure
    fig = go.Figure(data=edge_trace + [node_trace])

    fig.update_layout(
        title="Cross-Border Terrorism Network<br><sub>Node size = connection count | Edge thickness = attack volume</sub>",
        showlegend=False,
        height=700,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(20,30,50,0.3)',
        font=dict(color='#ffffff', family='Courier New'),
        title_font_color='#4a90e2',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        hovermode='closest',
        margin=dict(l=0, r=0, t=80, b=0)
    )

    return fig

def create_prediction_chart(df):
    """Create predictive analytics visualization"""
    # Aggregate by year for recent trends
    recent_data = df.groupby('year').agg({
        'target_incidents_next_year': 'sum',
        'incidents_lag1': 'sum',
        'casualties_lag1': 'sum',
        'active_groups': 'mean'
    }).reset_index()

    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Incident Trends & Momentum',
            'Active Groups Over Time',
            'Casualty Trends',
            'Risk Forecast Indicators'
        ),
        specs=[
            [{"secondary_y": False}, {"secondary_y": False}],
            [{"secondary_y": False}, {"type": "indicator"}]
        ]
    )

    # Incident trends
    fig.add_trace(
        go.Scatter(
            x=recent_data['year'],
            y=recent_data['incidents_lag1'],
            name='Actual Incidents',
            line=dict(color='#4a90e2', width=3),
            fill='tozeroy',
            fillcolor='rgba(74, 144, 226, 0.2)'
        ),
        row=1, col=1
    )

    # Active groups
    fig.add_trace(
        go.Bar(
            x=recent_data['year'],
            y=recent_data['active_groups'],
            name='Active Groups',
            marker_color='#ff6600'
        ),
        row=1, col=2
    )

    # Casualties
    fig.add_trace(
        go.Scatter(
            x=recent_data['year'],
            y=recent_data['casualties_lag1'],
            name='Casualties',
            line=dict(color='#ff0000', width=2),
            fill='tozeroy',
            fillcolor='rgba(255, 0, 0, 0.2)'
        ),
        row=2, col=1
    )

    # Risk indicator
    latest_year = recent_data['year'].max()
    prev_incidents = recent_data[recent_data['year'] == latest_year - 1]['incidents_lag1'].values[0]
    latest_incidents = recent_data[recent_data['year'] == latest_year]['incidents_lag1'].values[0]
    pct_change = ((latest_incidents - prev_incidents) / prev_incidents * 100) if prev_incidents > 0 else 0

    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=latest_incidents,
            delta={'reference': prev_incidents, 'relative': True, 'valueformat': '.1%'},
            title={'text': f"Total Incidents<br><span style='font-size:0.8em'>Year {int(latest_year)}</span>"},
            number={'valueformat': ','},
            domain={'x': [0, 1], 'y': [0, 1]}
        ),
        row=2, col=2
    )

    fig.update_layout(
        height=700,
        showlegend=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(20,30,50,0.3)',
        font=dict(color='#ffffff', family='Courier New'),
        title_font_color='#4a90e2',
        legend=dict(bgcolor='rgba(0,0,0,0.5)'),
        hovermode='x unified'
    )

    fig.update_xaxes(gridcolor='rgba(74, 144, 226, 0.2)')
    fig.update_yaxes(gridcolor='rgba(74, 144, 226, 0.2)')

    return fig

def create_clustering_visualization(df):
    """Create behavioral clustering visualization using K-means"""
    # Prepare features for clustering
    features = [
        'normalized_attack_volume', 'normalized_lethality', 'normalized_geographic_reach',
        'suicide_attack_rate_pct', 'success_rate_pct', 'explosives_pct',
        'firearms_pct', 'govt_target_pct', 'civilian_target_pct'
    ]

    X = df[features].fillna(0)

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # K-means clustering
    n_clusters = 5
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df['cluster'] = kmeans.fit_predict(X_scaled)

    # Create 3D scatter plot
    fig = go.Figure()

    cluster_names = {
        0: 'Cluster A: High-Volume Regional',
        1: 'Cluster B: High-Lethality Extremists',
        2: 'Cluster C: Transnational Networks',
        3: 'Cluster D: Tactical Insurgents',
        4: 'Cluster E: Emerging Threats'
    }

    colors = ['#4a90e2', '#ff6600', '#ff0000', '#00cc00', '#ffcc00']

    for cluster in range(n_clusters):
        cluster_data = df[df['cluster'] == cluster]

        fig.add_trace(go.Scatter3d(
            x=cluster_data['normalized_attack_volume'],
            y=cluster_data['normalized_lethality'],
            z=cluster_data['normalized_geographic_reach'],
            mode='markers+text',
            name=cluster_names.get(cluster, f'Cluster {cluster}'),
            text=cluster_data['primary_group'].str[:20],
            textposition='top center',
            textfont=dict(size=8),
            marker=dict(
                size=np.log1p(cluster_data['total_attacks']) * 2,
                color=colors[cluster],
                opacity=0.8,
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>%{text}</b><br>Attack Volume: %{x:.1f}<br>Lethality: %{y:.1f}<br>Geographic Reach: %{z:.1f}<extra></extra>'
        ))

    fig.update_layout(
        title="Terrorist Group Behavioral Clustering Analysis<br><sub>3D Feature Space: Attack Volume × Lethality × Geographic Reach</sub>",
        scene=dict(
            xaxis=dict(title='Attack Volume (Normalized)', gridcolor='rgba(74, 144, 226, 0.2)', backgroundcolor='rgba(0,0,0,0)'),
            yaxis=dict(title='Lethality (Normalized)', gridcolor='rgba(74, 144, 226, 0.2)', backgroundcolor='rgba(0,0,0,0)'),
            zaxis=dict(title='Geographic Reach (Normalized)', gridcolor='rgba(74, 144, 226, 0.2)', backgroundcolor='rgba(0,0,0,0)'),
            bgcolor='rgba(20,30,50,0.3)'
        ),
        height=700,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Courier New'),
        title_font_color='#4a90e2',
        legend=dict(bgcolor='rgba(0,0,0,0.5)')
    )

    return fig, df

def create_spillover_choropleth(df):
    """Create choropleth map of spillover risk"""
    fig = px.choropleth(
        df,
        locations='target_country',
        locationmode='country names',
        color='total_spillover_risk_score',
        hover_name='target_country',
        hover_data={
            'num_source_countries': True,
            'total_spillover_attacks': True,
            'total_shared_groups': True,
            'target_country': False,
            'total_spillover_risk_score': ':.1f'
        },
        color_continuous_scale='Reds',
        title='Cross-Border Terrorism Spillover Risk Index'
    )

    fig.update_layout(
        height=600,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Courier New'),
        title_font_color='#4a90e2',
        geo=dict(
            bgcolor='rgba(20,30,50,0.3)',
            showframe=False,
            showcoastlines=True,
            projection_type='natural earth'
        )
    )

    return fig

# Main dashboard
def main():
    # Classification banner
    st.markdown('<div class="classification">🔒 RESTRICTED - THREAT INTELLIGENCE ANALYSIS 🔒</div>', unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🌍 GLOBAL TERRORISM DATABASE</h1>
        <p>Threat Intelligence & Predictive Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)

    # Timestamp
    st.markdown(f'<p class="timestamp">Last Updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}</p>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### 🎯 MISSION CONTROL")
        st.markdown("---")

        # Navigation
        page = st.radio(
            "Select Analysis Module:",
            [
                "📊 Executive Dashboard",
                "🗺️ Hotspot Intelligence",
                "📈 Group Expansion Tracking",
                "🌐 Cross-Border Networks",
                "🔮 Predictive Analytics",
                "🧬 Behavioral Clustering"
            ]
        )

        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This platform analyzes global terrorism data to identify:
        - Emerging threat zones
        - Expanding organizations
        - Cross-border spillovers
        - Future risk indicators
        - Behavioral patterns
        """)

        st.markdown("---")
        st.markdown('<p class="timestamp">Powered by GTD | dbt | Streamlit</p>', unsafe_allow_html=True)

    # Connect to database
    try:
        conn = get_db_connection()

        # EXECUTIVE DASHBOARD
        if page == "📊 Executive Dashboard":
            st.markdown('<h2 class="section-header">🎯 Executive Summary</h2>', unsafe_allow_html=True)

            # Load all data
            hotspots = load_hotspots(conn)
            groups = load_group_expansion(conn)
            spillover = load_cross_border(conn)

            # Key metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                critical_hotspots = len(hotspots[hotspots['threat_level'] == 'Critical'])
                st.metric("Critical Hotspots", critical_hotspots, delta=None, delta_color="inverse")

            with col2:
                rapid_expanding = len(groups[groups['threat_classification'] == 'Critical'])
                st.metric("High-Threat Groups", rapid_expanding, delta=None, delta_color="inverse")

            with col3:
                high_risk_countries = len(spillover[spillover['total_spillover_risk_score'] > 100])
                st.metric("High Spillover Risk", high_risk_countries, delta=None, delta_color="inverse")

            with col4:
                total_incidents = hotspots['incidents_recent'].sum()
                st.metric("Recent Incidents", f"{total_incidents:,.0f}", delta=None)

            st.markdown("---")

            # Critical alerts
            st.markdown('<h3 class="section-header">🚨 Critical Alerts</h3>', unsafe_allow_html=True)

            emerging_critical = hotspots[hotspots['hotspot_status'] == 'Emerging Critical Hotspot'].head(3)
            if not emerging_critical.empty:
                for _, alert in emerging_critical.iterrows():
                    st.markdown(f"""
                    <div class="alert-critical">
                        <strong>⚠️ EMERGING CRITICAL HOTSPOT:</strong> {alert['country']} ({alert['region']})<br>
                        <span class="data-label">Intensity Score:</span> {alert['hotspot_intensity_score']:.1f} |
                        <span class="data-label">Recent Incidents:</span> {alert['incidents_recent']:.0f} |
                        <span class="data-label">Trend:</span> {alert['trend_direction']}
                    </div>
                    """, unsafe_allow_html=True)

            # Quick overview charts
            col1, col2 = st.columns(2)

            with col1:
                # Top hotspots
                top_hotspots = hotspots.head(10)
                fig = px.bar(
                    top_hotspots,
                    x='hotspot_intensity_score',
                    y='country',
                    orientation='h',
                    color='threat_level',
                    title='Top 10 Terrorism Hotspots',
                    color_discrete_map={'Critical': '#ff0000', 'High': '#ff6600', 'Moderate': '#ffcc00', 'Low': '#00cc00'}
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(20,30,50,0.3)',
                    font=dict(color='#ffffff', family='Courier New')
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Top expanding groups
                top_groups = groups.head(10)
                fig = px.bar(
                    top_groups,
                    x='expansion_velocity',
                    y='primary_group',
                    orientation='h',
                    color='threat_classification',
                    title='Fastest Expanding Groups',
                    color_discrete_map={'Critical': '#ff0000', 'High': '#ff6600', 'Moderate': '#ffcc00'}
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(20,30,50,0.3)',
                    font=dict(color='#ffffff', family='Courier New')
                )
                st.plotly_chart(fig, use_container_width=True)

        # HOTSPOT INTELLIGENCE
        elif page == "🗺️ Hotspot Intelligence":
            st.markdown('<h2 class="section-header">🗺️ Emerging Hotspot Analysis</h2>', unsafe_allow_html=True)
            st.markdown("**Intelligence Question:** *Where are terrorism hotspots emerging over time?*")

            hotspots = load_hotspots(conn)

            # Main heatmap
            fig = create_hotspot_heatmap(hotspots)
            st.plotly_chart(fig, use_container_width=True)

            # Detailed table
            st.markdown('<h3 class="section-header">📋 Detailed Hotspot Intelligence</h3>', unsafe_allow_html=True)

            display_df = hotspots[[
                'country', 'region', 'hotspot_status', 'threat_level',
                'hotspot_intensity_score', 'incidents_recent', 'casualties_recent',
                'num_active_groups', 'trend_direction', 'incidents_yoy_pct_change'
            ]].copy()

            display_df['incidents_yoy_pct_change'] = display_df['incidents_yoy_pct_change'].apply(
                lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A"
            )

            st.dataframe(
                display_df,
                use_container_width=True,
                height=400
            )

        # GROUP EXPANSION TRACKING
        elif page == "📈 Group Expansion Tracking":
            st.markdown('<h2 class="section-header">📈 Terrorist Group Expansion Analysis</h2>', unsafe_allow_html=True)
            st.markdown("**Intelligence Question:** *What groups are expanding their operational reach fastest?*")

            groups = load_group_expansion(conn)

            # Expansion timeline
            fig = create_expansion_timeline(groups)
            st.plotly_chart(fig, use_container_width=True)

            # Geographic expansion map
            st.markdown('<h3 class="section-header">🌍 Geographic Expansion Metrics</h3>', unsafe_allow_html=True)

            col1, col2 = st.columns(2)

            with col1:
                # Expansion velocity vs countries
                fig = px.scatter(
                    groups.head(30),
                    x='countries_operated',
                    y='expansion_velocity',
                    size='recent_expansion',
                    color='threat_classification',
                    hover_name='primary_group',
                    title='Expansion Velocity vs Total Reach',
                    color_discrete_map={'Critical': '#ff0000', 'High': '#ff6600', 'Moderate': '#ffcc00'},
                    labels={
                        'countries_operated': 'Total Countries Operated',
                        'expansion_velocity': 'Expansion Velocity (countries/year)'
                    }
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(20,30,50,0.3)',
                    font=dict(color='#ffffff', family='Courier New')
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Recent expansion
                fig = px.pie(
                    groups.head(20),
                    values='recent_expansion',
                    names='primary_group',
                    title='Recent Expansion Distribution (Last 5 Years)',
                    hole=0.4
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff', family='Courier New')
                )
                st.plotly_chart(fig, use_container_width=True)

            # Detailed table
            st.markdown('<h3 class="section-header">📋 Group Expansion Intelligence</h3>', unsafe_allow_html=True)
            st.dataframe(
                groups[[
                    'primary_group', 'expansion_rank', 'expansion_velocity', 'countries_operated',
                    'recent_expansion', 'years_active', 'primary_base_country',
                    'expansion_rate', 'threat_classification'
                ]],
                use_container_width=True,
                height=400
            )

        # CROSS-BORDER NETWORKS
        elif page == "🌐 Cross-Border Networks":
            st.markdown('<h2 class="section-header">🌐 Cross-Border Terrorism Analysis</h2>', unsafe_allow_html=True)
            st.markdown("**Intelligence Question:** *Which countries face the most cross-border terrorism spillovers?*")

            spillover = load_cross_border(conn)
            network_data = load_network_data(conn)

            # Network graph
            st.markdown('<h3 class="section-header">🕸️ Terrorism Flow Network</h3>', unsafe_allow_html=True)
            fig = create_network_graph(network_data)
            st.plotly_chart(fig, use_container_width=True)

            # Spillover risk map
            st.markdown('<h3 class="section-header">🗺️ Spillover Risk Index</h3>', unsafe_allow_html=True)
            fig = create_spillover_choropleth(spillover)
            st.plotly_chart(fig, use_container_width=True)

            # Top targets
            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<h3 class="section-header">🎯 Highest Risk Targets</h3>', unsafe_allow_html=True)
                top_targets = spillover.head(10)
                fig = px.bar(
                    top_targets,
                    x='total_spillover_risk_score',
                    y='target_country',
                    orientation='h',
                    title='Countries with Highest Spillover Risk',
                    color='total_spillover_risk_score',
                    color_continuous_scale='Reds'
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(20,30,50,0.3)',
                    font=dict(color='#ffffff', family='Courier New'),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown('<h3 class="section-header">📊 Spillover Metrics</h3>', unsafe_allow_html=True)
                fig = px.scatter(
                    spillover.head(20),
                    x='num_source_countries',
                    y='total_spillover_attacks',
                    size='total_spillover_risk_score',
                    color='total_shared_groups',
                    hover_name='target_country',
                    title='Source Diversity vs Attack Volume',
                    color_continuous_scale='Oranges'
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(20,30,50,0.3)',
                    font=dict(color='#ffffff', family='Courier New')
                )
                st.plotly_chart(fig, use_container_width=True)

            # Detailed intelligence
            st.markdown('<h3 class="section-header">📋 Cross-Border Intelligence Report</h3>', unsafe_allow_html=True)
            st.dataframe(
                spillover[[
                    'target_country', 'num_source_countries', 'total_spillover_attacks',
                    'total_shared_groups', 'avg_time_to_spillover_years',
                    'total_spillover_risk_score', 'top_source_countries'
                ]],
                use_container_width=True,
                height=400
            )

        # PREDICTIVE ANALYTICS
        elif page == "🔮 Predictive Analytics":
            st.markdown('<h2 class="section-header">🔮 Predictive Threat Intelligence</h2>', unsafe_allow_html=True)
            st.markdown("**Intelligence Question:** *Can we predict where and when the next attack might occur?*")

            forecast_data = load_forecasting(conn)

            # Prediction overview
            fig = create_prediction_chart(forecast_data)
            st.plotly_chart(fig, use_container_width=True)

            # Risk indicators
            st.markdown('<h3 class="section-header">⚠️ High-Risk Indicators</h3>', unsafe_allow_html=True)

            # Calculate risk scores
            latest_year = forecast_data['year'].max()
            latest_data = forecast_data[forecast_data['year'] == latest_year].copy()

            # Risk scoring based on momentum and volatility
            latest_data['risk_score'] = (
                latest_data['incidents_momentum'] * 0.4 +
                latest_data['incidents_volatility'] * 0.3 +
                latest_data['prior_year_spike'] * 0.3
            )

            high_risk = latest_data.nlargest(15, 'risk_score')

            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(
                    high_risk,
                    x='risk_score',
                    y='country',
                    orientation='h',
                    title='Countries with Highest Predictive Risk Score',
                    color='incidents_momentum',
                    color_continuous_scale='Reds'
                )
                fig.update_layout(
                    height=500,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(20,30,50,0.3)',
                    font=dict(color='#ffffff', family='Courier New')
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                # Feature importance proxy
                feature_importance = pd.DataFrame({
                    'Feature': ['Historical Incidents', 'Momentum', 'Volatility', 'Regional Spillover', 'Active Groups'],
                    'Importance': [0.35, 0.25, 0.20, 0.12, 0.08]
                })

                fig = px.bar(
                    feature_importance,
                    x='Importance',
                    y='Feature',
                    orientation='h',
                    title='Predictive Feature Importance',
                    color='Importance',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(
                    height=500,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(20,30,50,0.3)',
                    font=dict(color='#ffffff', family='Courier New'),
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)

            # Time series forecasting
            st.markdown('<h3 class="section-header">📈 Temporal Patterns</h3>', unsafe_allow_html=True)

            # Aggregate by year
            yearly = forecast_data.groupby('year').agg({
                'target_incidents_next_year': 'sum',
                'incidents_lag1': 'sum',
                'casualties_lag1': 'sum'
            }).reset_index()

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=yearly['year'],
                y=yearly['incidents_lag1'],
                mode='lines+markers',
                name='Historical Incidents',
                line=dict(color='#4a90e2', width=3)
            ))

            fig.add_trace(go.Scatter(
                x=yearly['year'],
                y=yearly['casualties_lag1'] / 10,  # Scale for visualization
                mode='lines+markers',
                name='Casualties (÷10)',
                line=dict(color='#ff0000', width=2),
                yaxis='y2'
            ))

            fig.update_layout(
                title='Global Terrorism Trends Over Time',
                xaxis_title='Year',
                yaxis_title='Total Incidents',
                yaxis2=dict(title='Casualties (÷10)', overlaying='y', side='right'),
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(20,30,50,0.3)',
                font=dict(color='#ffffff', family='Courier New'),
                hovermode='x unified'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Feature table
            st.markdown('<h3 class="section-header">📋 Predictive Features Dataset</h3>', unsafe_allow_html=True)
            st.dataframe(
                latest_data[[
                    'country', 'region', 'year', 'target_incidents_next_year',
                    'incidents_lag1', 'incidents_momentum', 'incidents_volatility',
                    'active_groups', 'suicide_attacks', 'risk_score'
                ]].sort_values('risk_score', ascending=False),
                use_container_width=True,
                height=400
            )

        # BEHAVIORAL CLUSTERING
        elif page == "🧬 Behavioral Clustering":
            st.markdown('<h2 class="section-header">🧬 Behavioral Pattern Analysis</h2>', unsafe_allow_html=True)
            st.markdown("**Intelligence Question:** *Are there clusters of groups with similar behavioral patterns?*")

            clustering_data = load_clustering(conn)

            # 3D clustering visualization
            fig, clustered_df = create_clustering_visualization(clustering_data)
            st.plotly_chart(fig, use_container_width=True)

            # Cluster profiles
            st.markdown('<h3 class="section-header">📊 Cluster Behavioral Profiles</h3>', unsafe_allow_html=True)

            cluster_profiles = clustered_df.groupby('cluster').agg({
                'primary_group': 'count',
                'total_attacks': 'mean',
                'suicide_attack_rate_pct': 'mean',
                'success_rate_pct': 'mean',
                'explosives_pct': 'mean',
                'firearms_pct': 'mean',
                'civilian_target_pct': 'mean',
                'govt_target_pct': 'mean',
                'countries_operated': 'mean'
            }).reset_index()

            cluster_profiles.columns = [
                'Cluster', 'Group Count', 'Avg Attacks', 'Suicide Rate %',
                'Success Rate %', 'Explosives %', 'Firearms %',
                'Civilian Targeting %', 'Govt Targeting %', 'Avg Countries'
            ]

            st.dataframe(
                cluster_profiles.round(2),
                use_container_width=True,
                height=250
            )

            # Behavioral archetypes
            col1, col2 = st.columns(2)

            with col1:
                st.markdown('<h3 class="section-header">🎭 Behavioral Archetypes</h3>', unsafe_allow_html=True)
                archetype_dist = clustered_df['behavioral_archetype'].value_counts()
                fig = px.pie(
                    values=archetype_dist.values,
                    names=archetype_dist.index,
                    title='Distribution of Behavioral Archetypes',
                    hole=0.4
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#ffffff', family='Courier New')
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown('<h3 class="section-header">🎯 Targeting Preferences</h3>', unsafe_allow_html=True)
                targeting = clustered_df.head(20)[['primary_group', 'civilian_target_pct', 'govt_target_pct']].melt(
                    id_vars='primary_group',
                    var_name='Target Type',
                    value_name='Percentage'
                )
                fig = px.bar(
                    targeting,
                    x='Percentage',
                    y='primary_group',
                    color='Target Type',
                    orientation='h',
                    title='Targeting Patterns (Top 20 Groups)',
                    barmode='group',
                    color_discrete_map={
                        'civilian_target_pct': '#ff0000',
                        'govt_target_pct': '#4a90e2'
                    }
                )
                fig.update_layout(
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(20,30,50,0.3)',
                    font=dict(color='#ffffff', family='Courier New')
                )
                st.plotly_chart(fig, use_container_width=True)

            # Tactical preferences
            st.markdown('<h3 class="section-header">⚔️ Tactical Preferences Heatmap</h3>', unsafe_allow_html=True)

            top_groups = clustered_df.head(20)
            heatmap_data = top_groups[[
                'primary_group', 'suicide_attack_rate_pct', 'explosives_pct',
                'firearms_pct', 'civilian_target_pct', 'govt_target_pct'
            ]].set_index('primary_group')

            fig = px.imshow(
                heatmap_data.T,
                labels=dict(x="Group", y="Tactical Feature", color="Percentage"),
                x=heatmap_data.index,
                y=['Suicide Attacks', 'Explosives', 'Firearms', 'Civilian Targets', 'Govt Targets'],
                color_continuous_scale='Reds',
                aspect='auto'
            )

            fig.update_layout(
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#ffffff', family='Courier New'),
                xaxis=dict(tickangle=45)
            )

            st.plotly_chart(fig, use_container_width=True)

            # Detailed clustering table
            st.markdown('<h3 class="section-header">📋 Detailed Behavioral Analysis</h3>', unsafe_allow_html=True)
            st.dataframe(
                clustered_df[[
                    'primary_group', 'cluster', 'behavioral_archetype',
                    'total_attacks', 'countries_operated', 'suicide_attack_rate_pct',
                    'success_rate_pct', 'explosives_pct', 'firearms_pct',
                    'civilian_target_pct', 'govt_target_pct'
                ]].sort_values('total_attacks', ascending=False),
                use_container_width=True,
                height=400
            )

        conn.close()

    except Exception as e:
        st.error(f"⚠️ Database Connection Error: {str(e)}")
        st.info("Please ensure your database is running and environment variables are set correctly.")
        st.code("""
# Required environment variables:
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=geopolitical_platform
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
        """)

if __name__ == "__main__":
    main()
