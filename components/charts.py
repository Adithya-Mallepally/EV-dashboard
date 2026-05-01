import plotly.express as px
import pandas as pd

COLORS = px.colors.qualitative.Bold

def chart_top_makes(df):
    """Bar chart: Top 10 EV makes by count."""
    counts = df["Make"].value_counts().head(10).reset_index()
    counts.columns = ["Make", "Count"]
    fig = px.bar(counts, x="Make", y="Count", color="Make",
                 color_discrete_sequence=COLORS,
                 title="Top 10 EV Makes by Fleet Count",
                 labels={"Count": "Number of Vehicles"})
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


def chart_adoption_trend(df):
    """Line chart: EV adoption over model years."""
    trend = df.groupby(["Model Year", "Electric Vehicle Type"]).size().reset_index(name="Count")
    fig = px.line(trend, x="Model Year", y="Count", color="Electric Vehicle Type",
                  markers=True, color_discrete_sequence=COLORS,
                  title="EV Adoption Trend by Model Year")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


def chart_range_scatter(df):
    """Scatter: Electric Range vs Model Year colored by EV type."""
    fig = px.scatter(df, x="Model Year", y="Electric Range",
                     color="Electric Vehicle Type", hover_data=["Make", "Model"],
                     color_discrete_sequence=COLORS, opacity=0.7,
                     title="Electric Range vs Model Year")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


def chart_range_boxplot(df):
    """Box plot: Electric Range distribution by top 8 makes."""
    top8 = df["Make"].value_counts().head(8).index.tolist()
    sub = df[df["Make"].isin(top8)]
    fig = px.box(sub, x="Make", y="Electric Range", color="Make",
                 color_discrete_sequence=COLORS,
                 title="Electric Range Distribution by Make (Top 8)")
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig


def chart_city_bubble(df):
    """Bubble chart: EV count by city."""
    if "City" not in df.columns:
        return None
    city_counts = df.groupby("City").size().reset_index(name="Count")
    fig = px.bar(city_counts.sort_values("Count", ascending=True).tail(10),
                 x="Count", y="City", orientation="h",
                 color="Count", color_continuous_scale="Blues",
                 title="Top Cities by EV Count")
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    return fig
