"""
tco_calculator.py
─────────────────
Total Cost of Ownership (TCO) and Environmental Carbon Offset Simulator.
Compares lifecycle economics and emissions between electric vehicles and
gasoline internal combustion engine (ICE) vehicles.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def calculate_tco(
    annual_miles: int = 12000,
    years: int = 5,
    gas_price_per_gal: float = 3.85,
    ice_mpg: float = 26.0,
    electricity_kwh_cost: float = 0.14,
    ev_kwh_per_100_miles: float = 30.0,
    ev_base_msrp: float = 45000.0,
    ice_base_msrp: float = 38000.0
):
    """Computes comparative multi-year operational and acquisition costs."""
    timeline = list(range(1, years + 1))

    # Annual fuel vs electricity
    annual_ice_fuel = (annual_miles / ice_mpg) * gas_price_per_gal
    annual_ev_electric = (annual_miles / 100.0) * ev_kwh_per_100_miles * electricity_kwh_cost

    # Annual maintenance (EV avg $0.06/mi vs ICE $0.10/mi)
    annual_ice_maint = annual_miles * 0.10
    annual_ev_maint = annual_miles * 0.06

    cumulative_ice = []
    cumulative_ev = []

    for y in timeline:
        total_ice = ice_base_msrp + (annual_ice_fuel + annual_ice_maint) * y
        total_ev = ev_base_msrp + (annual_ev_electric + annual_ev_maint) * y
        cumulative_ice.append(round(total_ice, 2))
        cumulative_ev.append(round(total_ev, 2))

    # Carbon emissions: 8,887 grams CO2 per gallon of gasoline
    annual_co2_kg_ice = (annual_miles / ice_mpg) * 8.887
    # US average grid emission: ~0.386 kg CO2 per kWh
    annual_co2_kg_ev = (annual_miles / 100.0) * ev_kwh_per_100_miles * 0.386
    annual_co2_saved_kg = max(0.0, annual_co2_kg_ice - annual_co2_kg_ev)
    total_co2_saved_metric_tons = (annual_co2_saved_kg * years) / 1000.0

    five_year_savings = cumulative_ice[-1] - cumulative_ev[-1]

    comparison_df = pd.DataFrame({
        "Year": timeline,
        "Gasoline ICE Vehicle ($)": cumulative_ice,
        "Electric Vehicle ($)": cumulative_ev
    })

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timeline, y=cumulative_ice,
        mode="lines+markers",
        name="Gasoline ICE Vehicle",
        line=dict(color="#d9381e", width=3)
    ))
    fig.add_trace(go.Scatter(
        x=timeline, y=cumulative_ev,
        mode="lines+markers",
        name="Electric Vehicle (EV)",
        line=dict(color="#1a73e8", width=3)
    ))

    fig.update_layout(
        title="Cumulative Total Cost of Ownership (TCO) Progression",
        xaxis_title="Ownership Duration (Years)",
        yaxis_title="Total Cumulative Cost ($ USD)",
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return {
        "comparison_df": comparison_df,
        "fig": fig,
        "net_savings": round(five_year_savings, 2),
        "co2_saved_tons": round(total_co2_saved_metric_tons, 2),
        "annual_fuel_savings": round(annual_ice_fuel - annual_ev_electric, 2),
        "annual_maint_savings": round(annual_ice_maint - annual_ev_maint, 2)
    }
