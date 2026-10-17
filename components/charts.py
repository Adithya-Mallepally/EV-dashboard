"""
components/charts.py
────────────────────
Plotly visualization engine styled with the DeLorean Marketplace design system.
Dark obsidian surfaces (#141417), DeLorean Redshift (#de1e14) and brushed steel palette,
Neue Haas Grotesk and TT Mussels typography, zero emojis and zero icons.
Fault-tolerant rendering with elegant empty-state handling.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# DeLorean Automotive Color Palette
DELOREAN_PALETTE = [
    "#de1e14",  # DeLorean Redshift (Taillight Crimson)
    "#e2e8f0",  # Brushed Stainless Steel
    "#38bdf8",  # Electric Cyan
    "#94a3b8",  # Slate Metallic
    "#f59e0b",  # Amber Dashboard Indicator
    "#a855f7",  # Ion Purple
    "#10b981",  # Efficiency Emerald
    "#64748b",  # Deep Steel
    "#f43f5e",  # Rose Accent
    "#06b6d4",  # Cyan Glow
]


def _apply_delorean_layout(fig, title_text: str):
    """Apply consistent DeLorean Marketplace theme to a Plotly figure."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#141417",
        title=dict(
            text=f"<span style='font-family: TTMussels, sans-serif; letter-spacing: 0.05em; font-weight: 700; color: #ffffff;'>{title_text.upper()}</span>",
            x=0.01,
            y=0.96,
            font=dict(size=13, color="#ffffff")
        ),
        font=dict(
            family="'NeueHaasGrotesk', 'Helvetica Neue', Arial, sans-serif",
            color="#a1a1aa",
            size=12
        ),
        xaxis=dict(
            gridcolor="#222228",
            zerolinecolor="#2e2e38",
            linecolor="#2c2c34",
            tickfont=dict(family="'MaisonNeueMono', monospace", size=11, color="#8e8e98")
        ),
        yaxis=dict(
            gridcolor="#222228",
            zerolinecolor="#2e2e38",
            linecolor="#2c2c34",
            tickfont=dict(family="'MaisonNeueMono', monospace", size=11, color="#8e8e98")
        ),
        legend=dict(
            font=dict(family="'MaisonNeueMono', monospace", size=11, color="#d4d4d8"),
            bgcolor="rgba(22, 22, 26, 0.7)",
            bordercolor="#27272f",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="#18181d",
            bordercolor="#3d3f47",
            font=dict(family="'MaisonNeueMono', monospace", size=12, color="#ffffff")
        ),
        margin=dict(l=40, r=20, t=50, b=40)
    )
    return fig


def _empty_figure(title_text: str):
    """Produce a graceful empty-state chart when filters produce zero records."""
    fig = go.Figure()
    _apply_delorean_layout(fig, title_text)
    fig.add_annotation(
        text="NO TELEMETRY RECORDS MATCH CURRENT FILTER SELECTION",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(family="'MaisonNeueMono', monospace", size=12, color="#71717a")
    )
    fig.update_xaxes(showgrid=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, showticklabels=False)
    return fig


def chart_top_makes(df: pd.DataFrame):
    """Bar chart: Top 10 EV makes by count."""
    if df.empty:
        return _empty_figure("Top 10 Manufacturers by Fleet Volume")

    counts = df["Make"].value_counts().head(10).reset_index()
    counts.columns = ["Make", "Count"]
    fig = px.bar(
        counts, x="Make", y="Count", color="Make",
        color_discrete_sequence=DELOREAN_PALETTE,
        labels={"Count": "FLEET COUNT", "Make": "MANUFACTURER"}
    )
    _apply_delorean_layout(fig, "Top 10 Manufacturers by Fleet Volume")
    fig.update_layout(showlegend=False)
    return fig


def chart_adoption_trend(df: pd.DataFrame):
    """Line chart: EV adoption over model years."""
    if df.empty:
        return _empty_figure("Registration Trajectory by Propulsion Type")

    trend = df.groupby(["Model Year", "Electric Vehicle Type"]).size().reset_index(name="Count")
    fig = px.line(
        trend, x="Model Year", y="Count", color="Electric Vehicle Type",
        markers=True, color_discrete_sequence=[DELOREAN_PALETTE[0], DELOREAN_PALETTE[2]],
        labels={"Count": "ANNUAL REGISTRATIONS", "Model Year": "MODEL YEAR", "Electric Vehicle Type": "PROPULSION ARCHITECTURE"}
    )
    _apply_delorean_layout(fig, "Registration Trajectory by Propulsion Type")
    return fig


def chart_range_scatter(df: pd.DataFrame):
    """Scatter: Electric Range vs Model Year colored by EV type."""
    if df.empty:
        return _empty_figure("EPA Range Dispersion Across Model Years")

    fig = px.scatter(
        df, x="Model Year", y="Electric Range",
        color="Electric Vehicle Type", hover_data=["Make", "Model"],
        color_discrete_sequence=[DELOREAN_PALETTE[0], DELOREAN_PALETTE[2]],
        opacity=0.75,
        labels={"Electric Range": "EPA RANGE (MILES)", "Model Year": "MODEL YEAR", "Electric Vehicle Type": "PROPULSION"}
    )
    _apply_delorean_layout(fig, "EPA Range Dispersion Across Model Years")
    return fig


def chart_range_boxplot(df: pd.DataFrame):
    """Box plot: Electric Range distribution by top 8 makes."""
    if df.empty:
        return _empty_figure("Range Variance Across Leading Manufacturers")

    top8 = df["Make"].value_counts().head(8).index.tolist()
    sub = df[df["Make"].isin(top8)]
    if sub.empty:
        return _empty_figure("Range Variance Across Leading Manufacturers")

    fig = px.box(
        sub, x="Make", y="Electric Range", color="Make",
        color_discrete_sequence=DELOREAN_PALETTE,
        labels={"Electric Range": "EPA RANGE (MILES)", "Make": "MANUFACTURER"}
    )
    _apply_delorean_layout(fig, "Range Variance Across Leading Manufacturers")
    fig.update_layout(showlegend=False)
    return fig


def chart_city_bubble(df: pd.DataFrame):
    """Bar chart: EV count by municipality."""
    if df.empty or "City" not in df.columns:
        return _empty_figure("Geographic Concentration by Municipality (Top 10)")

    city_counts = df.groupby("City").size().reset_index(name="Count")
    top_cities = city_counts.sort_values("Count", ascending=True).tail(10)

    # Redshift thermal gradient
    redshift_scale = [
        [0.0, "#22232a"],
        [0.4, "#5c1310"],
        [0.75, "#b8150d"],
        [1.0, "#de1e14"]
    ]

    fig = px.bar(
        top_cities, x="Count", y="City", orientation="h",
        color="Count", color_continuous_scale=redshift_scale,
        labels={"Count": "REGISTERED VEHICLES", "City": "MUNICIPALITY"}
    )
    _apply_delorean_layout(fig, "Geographic Concentration by Municipality (Top 10)")
    fig.update_coloraxes(colorbar=dict(
        title=dict(text="FLEET SIZE", font=dict(family="'MaisonNeueMono', monospace", size=10, color="#8e8e98")),
        tickfont=dict(family="'MaisonNeueMono', monospace", size=10, color="#8e8e98")
    ))
    return fig
