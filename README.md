# EV Fleet Analytics & Total Cost of Ownership Dashboard

An interactive analytics platform for exploring 8,000 Washington State Electric Vehicle registrations. Built with Python, Streamlit, Plotly, and scikit-learn. Combines fleet data engineering, interactive telemetry visualizations, machine learning range prediction, and an interactive Total Cost of Ownership (TCO) financial simulator.

---

## Unique Key Feature: Lifecycle TCO & Carbon Abatement Simulator

In addition to standard registration analytics, the dashboard includes an interactive Total Cost of Ownership (TCO) and Environmental Impact engine:
- Multi-Year Ownership Modeling: Dynamically computes cumulative acquisition, fuel, and maintenance costs comparing EV models against gasoline internal combustion engine (ICE) vehicles over 1-10 year horizons.
- Carbon Offset Quantification: Computes metric tons of greenhouse gas emissions avoided based on annual mileage, vehicle efficiency (kWh/100mi), and US electric grid emissions baselines.
- Real-Time Sensitivity Controls: Users can customize annual mileage, local electricity tariffs ($/kWh), and regional gasoline prices ($/gal) to calculate net financial break-even points.

---

## Features

- Interactive filters: Filter by Make, EV Type, Model Year, and Electric Range
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
├── app.py                      # Main Streamlit application entry point
├── data/
│   └── ev_data.csv             # 8,000-row EV registration dataset
├── components/
│   ├── filters.py              # Sidebar filter logic
│   ├── charts.py               # Plotly chart generation
│   ├── stats.py                # KPI computations
│   └── tco_calculator.py       # TCO & Carbon offset simulation engine
├── utils/
│   ├── data_loader.py          # Data cleaning and loading pipeline
│   └── ml_model.py             # Voting ensemble training and inference
├── requirements.txt
└── README.md
```

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
| Data Processing | Pandas 2.2, NumPy 1.26 |
| Visualizations | Plotly Express 5.22 |
| Machine Learning | scikit-learn 1.4 |

---

## Author

Roopadithya Vardhan Mallepally
M.Sc. Software Engineering - BTH Sweden
GitHub: https://github.com/Adithya-Mallepally
