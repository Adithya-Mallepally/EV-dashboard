import pandas as pd
import numpy as np
import os


def load_data(path="data/ev_data.csv"):
    """
    Load and clean the EV dataset.
    Falls back to generating realistic mock data if CSV not found.
    """
    if os.path.exists(path):
        df = pd.read_csv(path, low_memory=False)
    else:
        print("Dataset not found — generating mock data.")
        df = _generate_mock_data(600)

    df = _clean(df)
    return df.reset_index(drop=True)


def _clean(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and standardise the DataFrame."""
    df.columns = df.columns.str.strip()

    required = ["Make", "Model Year", "Electric Range", "Electric Vehicle Type"]
    df.dropna(subset=required, inplace=True)

    df["Model Year"] = pd.to_numeric(df["Model Year"], errors="coerce").astype("Int64")
    df["Electric Range"] = pd.to_numeric(df["Electric Range"], errors="coerce")
    df["Base MSRP"] = pd.to_numeric(df["Base MSRP"], errors="coerce")

    df = df[df["Electric Range"] > 0]
    df = df[df["Model Year"].between(2000, 2030)]
    df.dropna(subset=["Model Year", "Electric Range"], inplace=True)

    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    df["EV Type Short"] = df["Electric Vehicle Type"].apply(
        lambda x: "BEV" if "Battery" in str(x) else "PHEV"
    )

    return df


def _generate_mock_data(n=600):
    """Fallback: generate minimal realistic mock data."""
    np.random.seed(42)
    makes = ["Tesla", "Nissan", "Chevrolet", "BMW", "Ford",
             "Hyundai", "Kia", "Rivian", "Volkswagen", "Toyota"]
    rows = []
    for _ in range(n):
        make = np.random.choice(makes)
        year = int(np.random.choice(range(2015, 2025)))
        ev_type = np.random.choice(
            ["Battery Electric Vehicle (BEV)", "Plug-in Hybrid Electric Vehicle (PHEV)"],
            p=[0.72, 0.28]
        )
        base = 280 if make == "Tesla" else 200
        ev_range = int(np.clip(np.random.normal(base + (year - 2015) * 4, 25), 20, 420))
        rows.append({
            "Make": make, "Model": make + " EV", "Model Year": year,
            "Electric Vehicle Type": ev_type,
            "Electric Range": ev_range,
            "Base MSRP": int(np.random.normal(45000, 12000)),
            "City": "Seattle", "County": "King", "State": "WA",
        })
    return pd.DataFrame(rows)
