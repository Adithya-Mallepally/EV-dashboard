"""
utils/ml_model.py
─────────────────
Machine Learning module: trains a Random Forest + Gradient Boosting ensemble
to predict Electric Range from Make, Model, Model Year, EV Type, and Base MSRP.
Engineered with safe encoding for unseen categories and deterministic inference.
"""

import warnings
import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, VotingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

warnings.filterwarnings("ignore")


def _safe_transform(encoder: LabelEncoder, series: pd.Series, default: int = 0) -> pd.Series:
    """Safely map labels through encoder, falling back to default for unseen classes."""
    classes = set(encoder.classes_)
    return series.map(lambda x: encoder.transform([x])[0] if x in classes else default).astype(int)


def build_features(df: pd.DataFrame, le_make=None, le_model=None, le_type=None, fit: bool = True):
    """
    Engineer numerical feature matrix for model training and inference.
    Returns X (features matrix), le_make, le_model, le_type.
    """
    sub = df.copy()

    # Fill missing MSRP with median
    msrp_median = sub["Base MSRP"].median() if ("Base MSRP" in sub.columns and not sub["Base MSRP"].isna().all()) else 45000.0
    sub["Base MSRP"] = sub["Base MSRP"].fillna(msrp_median)
    sub["Base MSRP"] = sub["Base MSRP"].clip(10000, 250000)

    if le_make is None:
        le_make = LabelEncoder()
    if le_model is None:
        le_model = LabelEncoder()
    if le_type is None:
        le_type = LabelEncoder()

    if fit:
        sub["Make_enc"] = le_make.fit_transform(sub["Make"].astype(str))
        sub["Model_enc"] = le_model.fit_transform(sub["Model"].astype(str)) if "Model" in sub.columns else 0
        sub["Type_enc"] = le_type.fit_transform(sub["EV Type Short"].astype(str))
    else:
        sub["Make_enc"] = _safe_transform(le_make, sub["Make"].astype(str))
        sub["Model_enc"] = _safe_transform(le_model, sub["Model"].astype(str)) if "Model" in sub.columns else 0
        sub["Type_enc"] = _safe_transform(le_type, sub["EV Type Short"].astype(str))

    feature_cols = ["Make_enc", "Model_enc", "Model Year", "Type_enc", "Base MSRP"]
    X = sub[feature_cols].astype(float)
    return X, le_make, le_model, le_type


def train_model(df: pd.DataFrame):
    """
    Train a Voting Ensemble (Random Forest + Gradient Boosting) on EV registrations.
    Returns: model, le_make, le_model, le_type, metrics.
    """
    X, le_make, le_model, le_type = build_features(df, fit=True)
    y = df["Electric Range"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.15, random_state=42
    )

    rf = RandomForestRegressor(n_estimators=150, max_depth=12, random_state=42, n_jobs=-1)
    gb = GradientBoostingRegressor(n_estimators=150, max_depth=5, learning_rate=0.08, random_state=42)

    ensemble = VotingRegressor(estimators=[("rf", rf), ("gb", gb)])
    ensemble.fit(X_train, y_train)

    preds = ensemble.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    r2 = r2_score(y_test, preds)

    metrics = {
        "MAE (miles)": round(float(mae), 1),
        "R2 Score": round(float(r2), 3),
        "Test samples": len(y_test),
        "Train samples": len(y_train),
    }

    return ensemble, le_make, le_model, le_type, metrics


def predict_range(model, le_make, le_model, le_type, make: str, model_name: str, year: int, ev_type: str, msrp: float) -> int:
    """
    Predict electric range for a configured vehicle specification.
    Guaranteed non-negative integer output.
    """
    row = pd.DataFrame([{
        "Make": str(make),
        "Model": str(model_name),
        "Model Year": int(year),
        "EV Type Short": str(ev_type),
        "Base MSRP": float(msrp),
    }])
    X, _, _, _ = build_features(row, le_make=le_make, le_model=le_model, le_type=le_type, fit=False)
    pred = model.predict(X)[0]
    return max(0, int(round(pred)))
