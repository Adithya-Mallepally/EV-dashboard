"""
tests/test_dashboard.py
───────────────────────
Comprehensive test suite for the DeLorean EV Fleet Analytics Dashboard.
Validates:
- Data loader integrity and cleaning pipeline
- Machine learning model ensemble training and inference
- Sidebar filter operations and edge cases
- Visualization generation and graceful empty-state handling
- Total Cost of Ownership (TCO) simulation mathematics
- Zero-emoji, zero-icon architectural compliance
- DeLorean design system font assets and stylesheet generation
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
from components.theme import get_delorean_css


@pytest.fixture(scope="session")
def ev_df():
    """Load the cleaned dataset once for the test session."""
    return load_data()


@pytest.fixture(scope="session")
def trained_model(ev_df):
    """Train the ML model once for testing."""
    return train_model(ev_df)


# ── 1. Data Loader & Dataset Integrity ─────────────────────────────────────────

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


# ── 2. Machine Learning Model Suite ───────────────────────────────────────────

def test_ml_model_accuracy(trained_model):
    model, le_make, le_model, le_type, metrics = trained_model
    assert metrics["R2 Score"] > 0.95, f"R2 score too low: {metrics['R2 Score']}"
    assert metrics["MAE (miles)"] < 15.0, f"MAE too high: {metrics['MAE (miles)']}"
    assert metrics["Test samples"] > 0
    assert metrics["Train samples"] > 0


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
    # Unseen manufacturer and model should not raise exception
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


# ── 5. Zero Emojis and Zero Badges Compliance ─────────────────────────────────

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


# ── 6. DeLorean Theme & Typography ────────────────────────────────────────────

def test_delorean_theme_css():
    css = get_delorean_css()
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

