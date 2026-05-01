import streamlit as st

def render_kpis(df):
    """Render top KPI metric cards from filtered DataFrame."""
    total = len(df)
    avg_range = df["Electric Range"].mean() if total > 0 else 0
    top_make = df["Make"].value_counts().idxmax() if total > 0 else "N/A"

    bev_count = len(df[df["Electric Vehicle Type"].str.startswith("Battery")])
    bev_pct = (bev_count / total * 100) if total > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🚗 Total Vehicles", f"{total:,}")
    col2.metric("🛣️ Avg Electric Range", f"{avg_range:.0f} mi")
    col3.metric("🏆 Top Make", top_make)
    col4.metric("⚡ BEV Share", f"{bev_pct:.1f}%")
