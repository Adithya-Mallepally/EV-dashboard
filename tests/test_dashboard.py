"""
tests/test_dashboard.py
───────────────────────
Comprehensive automated test suite for the Washington State EV Fleet Analytics Dashboard.
Validates:
- Data loader integrity, cleaning pipeline, and multi-parameter filtering
- Machine learning model ensemble training, feature encoding, and range inference
- Telemetry KPI computation accuracy
- Visualizations generation, layout consistency, and graceful empty-state handling
- Total Cost of Ownership (TCO) simulation mathematics and monotonic savings
- Strict zero-emoji and zero-icon architectural compliance
- Dark automotive design system font assets and stylesheet generation
- Absence of stray prototype or reference branding in user-facing copy
"""

import os
import re
import pytest
import pandas as pd
import plotly.graph_objects as go

from utils.data_loader import load_data, _clean
from utils.ml_model import train_model, predict_range, build_features
from components.charts import (
    chart_top_makes, chart_adoption_trend,
    chart_range_scatter, chart_range_boxplot, chart_city_bubble
)
from components.tco_calculator import calculate_tco
from components.theme import get_theme_css


@pytest.fixture(scope="session")
def ev_df():
    """Load the cleaned dataset once for the test session."""
    return load_data()


@pytest.fixture(scope="session")
def trained_model(ev_df):
    """Train the ML model once for testing."""
    return train_model(ev_df)


# ── 1. Data Loader & Ingestion Integrity ───────────────────────────────────────

def test_data_loader_shape_and_records(ev_df):
    assert len(ev_df) == 8000, f"Expected 8000 records, got {len(ev_df)}"
    assert ev_df["Electric Range"].min() > 0, "All vehicles must have positive range"
    assert ev_df["Model Year"].min() >= 2000, "Model year must be valid"


def test_data_loader_required_columns(ev_df):
    expected_cols = [
        "Make", "Model", "Model Year", "Electric Vehicle Type",
        "Electric Range", "Base MSRP", "City", "County", "State", "EV Type Short"
    ]
    for col in expected_cols:
        assert col in ev_df.columns, f"Missing required column: {col}"


def test_data_loader_clean_helper():
    raw_df = pd.DataFrame({
        " Make ": [" Tesla "],
        " Model Year ": [" 2023 "],
        " Electric Range ": [" 300 "],
        " Electric Vehicle Type ": [" Battery Electric Vehicle (BEV) "],
        " Base MSRP ": [" 55000 "]
    })
    cleaned = _clean(raw_df)
    assert cleaned["Make"].iloc[0] == "Tesla"
    assert cleaned["EV Type Short"].iloc[0] == "BEV"
    assert cleaned["Electric Range"].iloc[0] == 300


def test_data_loader_filter_simulation(ev_df):
    selected_makes = ["Tesla", "Nissan"]
    selected_types = ["Battery Electric Vehicle (BEV)"]
    year_range = (2018, 2023)
    range_filter = (150, 400)

    filtered = ev_df[
        ev_df["Make"].isin(selected_makes) &
        ev_df["Electric Vehicle Type"].isin(selected_types) &
        ev_df["Model Year"].between(*year_range) &
        ev_df["Electric Range"].between(*range_filter)
    ]
    assert len(filtered) > 0, "Filter should yield records"
    assert set(filtered["Make"].unique()).issubset(set(selected_makes))
    assert set(filtered["Electric Vehicle Type"].unique()) == set(selected_types)
    assert filtered["Model Year"].min() >= 2018
    assert filtered["Model Year"].max() <= 2023
    assert filtered["Electric Range"].min() >= 150
    assert filtered["Electric Range"].max() <= 400


# ── 2. Machine Learning Model Suite ───────────────────────────────────────────

def test_ml_model_accuracy(trained_model):
    model, le_make, le_model, le_type, metrics = trained_model
    assert metrics["R2 Score"] > 0.95, f"R2 score too low: {metrics['R2 Score']}"
    assert metrics["MAE (miles)"] < 15.0, f"MAE too high: {metrics['MAE (miles)']}"
    assert metrics["Test samples"] > 0
    assert metrics["Train samples"] > 0


def test_ml_build_features_schema(ev_df):
    X, le_make, le_model, le_type = build_features(ev_df)
    assert len(X) == len(ev_df)
    expected_features = ["Make_enc", "Model_enc", "Model Year", "Type_enc", "Base MSRP"]
    assert list(X.columns) == expected_features
    assert not X.isnull().values.any(), "Feature matrix contains unexpected nulls"


def test_ml_predict_range_valid(trained_model):
    model, le_make, le_model, le_type, _ = trained_model
    pred = predict_range(
        model, le_make, le_model, le_type,
        make="Tesla", model_name="Model 3", year=2023, ev_type="BEV", msrp=45000
    )
    assert isinstance(pred, int)
    assert 150 <= pred <= 450, f"Unexpected predicted range: {pred}"


def test_ml_predict_unseen_make_and_model(trained_model):
    model, le_make, le_model, le_type, _ = trained_model
    pred = predict_range(
        model, le_make, le_model, le_type,
        make="UnseenFuturisticMake", model_name="Hyperion", year=2024, ev_type="BEV", msrp=60000
    )
    assert isinstance(pred, int)
    assert pred >= 0


# ── 3. Visualizations Suite & Empty State Resilience ──────────────────────────

def test_charts_with_normal_data(ev_df):
    f1 = chart_top_makes(ev_df)
    f2 = chart_adoption_trend(ev_df)
    f3 = chart_range_scatter(ev_df)
    f4 = chart_range_boxplot(ev_df)
    f5 = chart_city_bubble(ev_df)

    for fig in [f1, f2, f3, f4, f5]:
        assert fig is not None
        assert isinstance(fig, go.Figure)


def test_charts_with_empty_data():
    empty = pd.DataFrame(columns=[
        "Make", "Model", "Model Year", "Electric Range",
        "Electric Vehicle Type", "Base MSRP", "City"
    ])
    f1 = chart_top_makes(empty)
    f2 = chart_adoption_trend(empty)
    f3 = chart_range_scatter(empty)
    f4 = chart_range_boxplot(empty)
    f5 = chart_city_bubble(empty)

    for fig in [f1, f2, f3, f4, f5]:
        assert fig is not None
        assert isinstance(fig, go.Figure)


def test_automotive_chart_layout_properties(ev_df):
    fig = chart_top_makes(ev_df)
    layout = fig.layout
    assert layout.paper_bgcolor == "rgba(0,0,0,0)"
    assert layout.plot_bgcolor == "#141417"
    assert "NeueHaasGrotesk" in str(layout.font.family)


# ── 4. Total Cost of Ownership (TCO) Simulator ────────────────────────────────

def test_tco_calculator_normal():
    res = calculate_tco(annual_miles=12000, years=5, gas_price_per_gal=3.85, ev_base_msrp=45000.0)
    assert "fig" in res
    assert "net_savings" in res
    assert "co2_saved_tons" in res
    assert res["co2_saved_tons"] > 0
    assert res["annual_fuel_savings"] > 0
    assert len(res["comparison_df"]) == 5


def test_tco_calculator_edge_cases():
    res = calculate_tco(annual_miles=0, years=0, gas_price_per_gal=-1.0, ice_mpg=0.0)
    assert res["net_savings"] is not None
    assert isinstance(res["fig"], go.Figure)


def test_tco_fuel_savings_monotonic():
    res = calculate_tco(annual_miles=15000, years=6, gas_price_per_gal=4.00, electricity_kwh_cost=0.12, ice_base_msrp=40000.0, ev_base_msrp=40000.0)
    df = res["comparison_df"]
    savings = df["Gasoline ICE Vehicle ($)"] - df["Electric Vehicle ($)"]
    assert savings.is_monotonic_increasing, "Cumulative savings must increase monotonically each year"


# ── 5. Telemetry & KPI Computations ───────────────────────────────────────────

def test_kpi_card_data_computation(ev_df):
    total = len(ev_df)
    avg_range = ev_df["Electric Range"].mean()
    top_make = ev_df["Make"].value_counts().idxmax()
    bev_count = len(ev_df[ev_df["Electric Vehicle Type"].str.startswith("Battery")])
    bev_pct = (bev_count / total * 100)

    assert total == 8000
    assert avg_range > 100
    assert top_make.upper() == "TESLA"
    assert 60.0 <= bev_pct <= 90.0


# ── 6. Zero Emojis and Zero Icons Architectural Compliance ───────────────────

def test_zero_emojis_in_source_code():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\ud83c-\ud83e]')

    for root, _, files in os.walk(project_dir):
        if any(p in root for p in [".git", "venv", ".venv", "__pycache__", "assets"]):
            continue
        for f in files:
            if f.endswith((".py", ".md", ".toml", ".txt")):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    text = fh.read()
                emojis = emoji_pattern.findall(text)
                assert len(emojis) == 0, f"Found emojis in {f}: {emojis}"


def test_zero_icons_compliance():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_dirs = ["components", "utils", "static"]
    target_files = ["app.py", "README.md"]
    forbidden_icon_indicators = ["font-awesome", "feather-icon", "material-symbols", "lucide"]

    # Verify no icon libraries in target code and doc files
    for d in target_dirs:
        dir_path = os.path.join(project_dir, d)
        if not os.path.exists(dir_path):
            continue
        for root, _, files in os.walk(dir_path):
            for f in files:
                if f.endswith((".py", ".html")):
                    p = os.path.join(root, f)
                    with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                        content = fh.read().lower()
                    for ind in forbidden_icon_indicators:
                        assert ind not in content, f"Found icon reference '{ind}' in {f}"

    for tf in target_files:
        p = os.path.join(project_dir, tf)
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read().lower()
            for ind in forbidden_icon_indicators:
                assert ind not in content, f"Found icon reference '{ind}' in {tf}"


# ── 7. Dark Automotive Design System & Typography ─────────────────────────────

def test_theme_css_palette_and_fonts():
    css = get_theme_css()
    assert "TTMussels" in css
    assert "NeueHaasGrotesk" in css
    assert "MaisonNeueMono" in css
    assert "#0e0e11" in css
    assert "#de1e14" in css


def test_font_files_exist():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fonts_dir = os.path.join(project_dir, "assets", "fonts")
    required_fonts = [
        "NeueHaasGrotesk.ttf",
        "NeueHaasGroteskBold.ttf",
        "TTMussels.otf",
        "MaisonNeueMono.otf"
    ]
    for font in required_fonts:
        p = os.path.join(fonts_dir, font)
        assert os.path.exists(p), f"Font file missing: {font}"
        assert os.path.getsize(p) > 10000, f"Font file too small: {font}"


def test_no_delorean_in_user_facing_copy():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(project_dir, "app.py"), "r", encoding="utf-8") as f:
        app_text = f.read()
    assert "DELOREAN MOTOR COMPANY" not in app_text
    assert 'page_title="DeLorean' not in app_text
    assert "<span>DELOREAN</span>" not in app_text
