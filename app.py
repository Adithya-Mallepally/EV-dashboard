import streamlit as st
import pandas as pd

from utils.data_loader import load_data
from utils.ml_model import train_model, predict_range
from components.filters import render_filters
from components.stats import render_kpis
from components.charts import (
    chart_top_makes, chart_adoption_trend,
    chart_range_scatter, chart_range_boxplot, chart_city_bubble
)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EV Fleet Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .stMetric { background: #f0f4ff; border-radius: 10px; padding: 8px; }
    section[data-testid="stSidebar"] { background: #0d1b2a; color: white; }
    section[data-testid="stSidebar"] * { color: white !important; }
    h1, h2, h3 { color: #1a73e8; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

@st.cache_resource
def get_model(df):
    return train_model(df)

df = get_data()
model, le_make, le_model, le_type, metrics = get_model(df)

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("## ⚡ EV Fleet Dashboard")
st.sidebar.markdown("---")
filtered_df = render_filters(df)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("⚡ EV Fleet Analytics Dashboard")
st.markdown("Interactive analysis of **8,000 Washington State EV registrations** — trends, range, fleet distribution, and ML-powered predictions.")
st.markdown("---")

# ── KPIs ──────────────────────────────────────────────────────────────────────
render_kpis(filtered_df)
st.markdown("---")

# ── Charts Row 1 ─────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(chart_top_makes(filtered_df), use_container_width=True)
with col2:
    st.plotly_chart(chart_adoption_trend(filtered_df), use_container_width=True)

# ── Charts Row 2 ─────────────────────────────────────────────────────────────
col3, col4 = st.columns(2)
with col3:
    st.plotly_chart(chart_range_scatter(filtered_df), use_container_width=True)
with col4:
    st.plotly_chart(chart_range_boxplot(filtered_df), use_container_width=True)

# ── City chart ────────────────────────────────────────────────────────────────
city_fig = chart_city_bubble(filtered_df)
if city_fig:
    st.plotly_chart(city_fig, use_container_width=True)

st.markdown("---")

# ── ML Predictor ─────────────────────────────────────────────────────────────
st.markdown("### 🤖 Electric Range Predictor")

mc1, mc2, mc3 = st.columns(3)
with mc1:
    st.metric("Model",         "RandomForest + GradientBoosting Ensemble")
with mc2:
    st.metric("R² Score",      str(metrics["R² Score"]))
with mc3:
    st.metric("Mean Abs Error", f"{metrics['MAE (miles)']} miles")

st.markdown("---")
st.markdown("#### Configure a Vehicle")

p1, p2, p3, p4, p5 = st.columns(5)
with p1:
    pred_make = st.selectbox("Make", sorted(df["Make"].unique()))
with p2:
    models_for_make = sorted(df[df["Make"] == pred_make]["Model"].unique())
    pred_model = st.selectbox("Model", models_for_make)
with p3:
    pred_year = st.slider("Year", int(df["Model Year"].min()), 2025, 2023)
with p4:
    pred_ev_type = st.selectbox("EV Type", ["BEV", "PHEV"])
with p5:
    pred_msrp = st.number_input("Base MSRP ($)", min_value=15000, max_value=250000,
                                 value=45000, step=1000)

if st.button("⚡ Predict Electric Range", type="primary"):
    try:
        pred = predict_range(model, le_make, le_model, le_type,
                             pred_make, pred_model, pred_year, pred_ev_type, pred_msrp)
        st.success(f"🔋 Predicted Electric Range: **{pred} miles**")
        st.caption("Based on ensemble model trained on 6,800 real EV registrations.")
    except Exception as e:
        st.warning(f"Could not predict: {e}")

st.markdown("---")

# ── Data Table ────────────────────────────────────────────────────────────────
if st.checkbox("📋 Show Raw Data Table"):
    st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

csv = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download Filtered Data as CSV", csv, "ev_filtered.csv", "text/csv")

st.markdown("<br><center><sub>Dataset: Washington State EV Population (8,000 records) | Built with Streamlit, Plotly & scikit-learn</sub></center>",
            unsafe_allow_html=True)
