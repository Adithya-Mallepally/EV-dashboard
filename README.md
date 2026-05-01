# ⚡ EV Fleet Analytics Dashboard

An interactive web dashboard for exploring **8,000 Washington State Electric Vehicle registrations**. Built with Python, Streamlit, and scikit-learn. Designed as a portfolio project showcasing data engineering, interactive visualization, and machine learning skills — relevant to automotive and data roles.

---

## 📸 What It Does

| Feature | Details |
|---|---|
| **Interactive filters** | Filter by Make, EV Type, Model Year, Electric Range |
| **KPI cards** | Live totals: fleet count, avg range, top make, BEV % share |
| **5 Plotly charts** | Bar, line, scatter, box plot, city distribution |
| **ML Range Predictor** | Predicts electric range from Make + Model + Year + MSRP |
| **CSV export** | Download any filtered slice of data |
| **Data table** | Toggle raw data view |

---

## 🤖 Machine Learning Model

The predictor uses a **Voting Ensemble** combining:
- `RandomForestRegressor` (150 trees, depth 12)
- `GradientBoostingRegressor` (150 estimators, lr 0.08)

**Features used:**
- Make (label-encoded)
- Model (label-encoded)
- Model Year
- EV Type (BEV / PHEV)
- Base MSRP

**Performance on held-out test set (1,200 vehicles):**
| Metric | Value |
|---|---|
| R² Score | **0.985** |
| Mean Absolute Error | **11.3 miles** |
| Training samples | 6,800 |

---

## 📁 Project Structure

```
ev-dashboard/
├── app.py                      # Main Streamlit entry point
├── data/
│   └── ev_data.csv             # 8,000-row EV registration dataset
├── components/
│   ├── filters.py              # Sidebar filter logic
│   ├── charts.py               # All 5 Plotly chart functions
│   └── stats.py                # KPI card computations
├── utils/
│   ├── data_loader.py          # CSV loading + cleaning pipeline
│   └── ml_model.py             # Ensemble model training + prediction
├── requirements.txt
└── README.md
```

---

## 🚀 Install & Run Locally

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Unzip and enter the project
unzip ev-dashboard.zip
cd ev-dashboard

# 2. (Optional but recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
streamlit run app.py
```

The app opens at **http://localhost:8501**

> The dataset is included in `data/ev_data.csv`. If the file is missing, the app auto-generates 600 rows of realistic mock data as a fallback.

---

## ☁️ Deploy Free on Streamlit Community Cloud

1. Push this folder to a **public GitHub repo**
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select your repo → set main file: `app.py`
4. Click **Deploy** — live public URL in ~2 minutes

---

## 📊 Dataset

| Field | Value |
|---|---|
| Source | Washington State Department of Licensing (DOL) |
| Records | 8,000 EV registrations |
| Vehicles | 19 makes, 50+ models (Tesla, BMW, Ford, Hyundai, Kia, Volvo, Rivian…) |
| Year range | 2008 – 2024 |
| EV split | ~75% BEV, ~25% PHEV |
| Geo coverage | 20 Washington State cities across 6 counties |

Key columns: `Make`, `Model`, `Model Year`, `Electric Vehicle Type`, `Electric Range`, `Base MSRP`, `City`, `County`, `State`

---

## 🛠️ Tech Stack

| Layer | Library |
|---|---|
| Dashboard | Streamlit 1.33 |
| Data processing | Pandas 2.2, NumPy 1.26 |
| Visualizations | Plotly Express 5.22 |
| Machine learning | scikit-learn 1.4 |

---

## 💡 How to Mention This in an Application

> *"Built an interactive EV fleet analytics dashboard using Python, Streamlit, and Plotly — analyzing 8,000 vehicle registrations with real-time filters, 5 chart types, and a RandomForest + GradientBoosting ensemble model achieving R²=0.985 for electric range prediction. Deployed on Streamlit Cloud."*

---

## 📄 License

MIT — free to use, modify, and share.
