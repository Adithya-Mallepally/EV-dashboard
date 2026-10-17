# EV Fleet Analytics & Total Cost of Ownership Dashboard

An interactive analytics platform for exploring 8,000 Washington State Electric Vehicle registrations. Built with Python, Streamlit, Plotly, and scikit-learn. Features a dark minimalist automotive telemetry interface with authentic typography, machine learning range forecasting, and an interactive Total Cost of Ownership (TCO) financial simulator.

---

## User Interface & Design System: Minimalist Automotive Aesthetic

The user interface features a high-end dark automotive telemetry design system:
- Authentic Typography:
  - Primary Interface & Titles: Neue Haas Grotesk TX Pro (Regular & Bold)
  - Telemetry & Numeric Readouts: Maison Neue Mono
  - Secondary Display: TT Mussels
- Obsidian Dark Palette:
  - Background: Obsidian Carbon (#0e0e11)
  - Surface Containers: Dark Slate (#16161a) with subtle industrial borders (#27272f)
  - Primary Accent: Crimson Redshift (#de1e14)
  - Metallic Accents: Brushed Stainless Steel (#e2e8f0) and Cyber Cyan (#38bdf8)
- Minimalist Technical Precision: Zero emojis and zero icons across all UI components, metric cards, charts, and telemetry readouts.


---

## Unique Key Feature: Lifecycle TCO & Carbon Abatement Simulator

In addition to standard registration analytics, the dashboard includes an interactive Total Cost of Ownership (TCO) and Environmental Impact engine:
- Multi-Year Ownership Modeling: Dynamically computes cumulative acquisition, fuel, and maintenance costs comparing EV models against gasoline internal combustion engine (ICE) vehicles over 1-10 year horizons.
- Carbon Offset Quantification: Computes metric tons of greenhouse gas emissions avoided based on annual mileage, vehicle efficiency (kWh/100mi), and US electric grid emissions baselines.
- Real-Time Sensitivity Controls: Users can customize annual mileage, local electricity tariffs ($/kWh), and regional gasoline prices ($/gal) to calculate net financial break-even points.

---

## Features

- Interactive filters: Filter by Manufacturer, Propulsion Type, Model Year Horizon, and Electric Range
- KPI summary cards: Live counts of fleet size, average range, leading manufacturer, and BEV market share
- Five Plotly analytical charts: Distribution bar chart, adoption trajectory, range vs MSRP scatter, box plot, and geographic bubble map
- Ensemble ML Range Predictor: Voting regressor combining Random Forest and Gradient Boosting to predict range from vehicle specifications
- TCO and Carbon Offset Simulator: Comparative financial curves and greenhouse gas abatement modeling
- CSV export: Download any filtered dataset slice
- Raw data toggle: Inspect raw tabular registration records

---

## Machine Learning Model

The predictor uses a Voting Ensemble combining:
- RandomForestRegressor (150 trees, max depth 12)
- GradientBoostingRegressor (150 estimators, learning rate 0.08)

Features used:
- Make (label-encoded)
- Model (label-encoded)
- Model Year
- EV Type (BEV / PHEV)
- Base MSRP

Performance on held-out test set (1,200 vehicles):
- R2 Score: 0.985
- Mean Absolute Error: 11.3 miles
- Training samples: 6,800 records

---

## Project Structure

```
ev-dashboard/
├── .github/
│   └── workflows/
│       └── ci.yml              # Automated testing & code hygiene verification
├── .streamlit/
│   └── config.toml             # Native Streamlit dark theme configuration
├── assets/
│   └── fonts/                  # Authentic automotive webfonts
│       ├── NeueHaasGrotesk.ttf
│       ├── NeueHaasGroteskBold.ttf
│       ├── TTMussels.otf
│       └── MaisonNeueMono.otf
├── app.py                      # Main Streamlit application entry point
├── data/
│   └── ev_data.csv             # 8,000-row EV registration dataset
├── components/
│   ├── theme.py                # Automotive telemetry design system & font injection
│   ├── filters.py              # Sidebar filter logic
│   ├── charts.py               # Plotly chart generation (dark obsidian palette)
│   ├── stats.py                # KPI computations and telemetry metric cards
│   └── tco_calculator.py       # TCO & Carbon offset simulation engine
├── tests/
│   ├── conftest.py             # Test discovery and module anchoring
│   └── test_dashboard.py       # Automated test suite (20 unit tests)
├── utils/
│   ├── data_loader.py          # Data cleaning and loading pipeline
│   └── ml_model.py             # Voting ensemble training and inference
├── TEST_REPORT.md              # Comprehensive test execution & validation report
├── requirements.txt
└── README.md
```

---

## Automated Test Coverage & Verification

All test suites execute via pytest with 100% pass rate:

```bash
python -m pytest -v tests/test_dashboard.py
```

| Test Domain | Tests | Scope | Status |
|---|---|---|---|
| Data Ingestion & Integrity | 4 | 8,000 records verification, column schemas, data cleaning, multi-parameter filtering | Passed |
| Machine Learning Pipeline | 4 | Ensemble accuracy (R2 > 0.95), feature matrix encoding, deterministic & unseen inference | Passed |
| Plotly Visualizations | 3 | 5 analytical charts generation, empty-state fallback resilience, automotive layout styling | Passed |
| TCO Financial Simulator | 3 | 10-year lifecycle simulation, boundary condition handling, monotonic savings verification | Passed |
| Telemetry KPI Readouts | 1 | Real-time fleet population, mean range, leading make, and BEV market share accuracy | Passed |
| Zero Emojis & Zero Icons | 2 | Unicode codebase scan, icon library audit, strictly technical typography | Passed |
| Design System & Typography | 3 | CSS stylesheet variables, physical font asset integrity, clean copy verification | Passed |
| **Total** | **20** | **Comprehensive end-to-end coverage across data, ML, UI, and design compliance** | **20 Passed, 0 Failed** |

Detailed assertion documentation and performance metrics are recorded in [TEST_REPORT.md](TEST_REPORT.md).

---

## Installation & Local Execution

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone repository
git clone https://github.com/Adithya-Mallepally/EV-dashboard.git
cd EV-dashboard

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the application
streamlit run app.py
```

The application will be accessible at http://localhost:8501

---

## Dataset

- Source: Washington State Department of Licensing (DOL)
- Records: 8,000 EV registrations
- Coverage: 19 makes, 50+ models (Tesla, BMW, Ford, Hyundai, Kia, Volvo, Rivian, etc.)
- Model Years: 2008 - 2024
- Powertrain Split: ~75% Battery Electric (BEV), ~25% Plug-in Hybrid (PHEV)
- Geographic Coverage: 20 Washington State cities across 6 counties

Key attributes: Make, Model, Model Year, Electric Vehicle Type, Electric Range, Base MSRP, City, County, State.

---

## Tech Stack

| Layer | Library |
|---|---|
| Dashboard | Streamlit 1.33 |
| Design System | Minimalist Automotive UI (Neue Haas Grotesk, Maison Neue Mono) |
| Data Processing | Pandas 2.2, NumPy 1.26 |
| Visualizations | Plotly Express 5.22 |
| Machine Learning | scikit-learn 1.4 |

---

## Author

Roopadithya Vardhan Mallepally
M.Sc. Software Engineering - BTH Sweden
GitHub: https://github.com/Adithya-Mallepally
