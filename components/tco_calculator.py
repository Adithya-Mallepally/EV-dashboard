"""
components/tco_calculator.py
────────────────────────────
Total Cost of Ownership (TCO) and Environmental Carbon Offset Simulator.
Compares lifecycle economics and emissions between electric vehicles and
gasoline internal combustion engine (ICE) vehicles.
Styled for DeLorean Marketplace UI: obsidian surfaces, Redshift accent,
zero emojis, zero icons, TT Mussels and Maison Neue Mono typography.
"""

import pandas as pd
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
    """Computes comparative multi-year operational and acquisition costs with input validation."""
    # Defend against division by zero or negative inputs
    annual_miles = max(100, int(annual_miles))
    years = max(1, min(15, int(years)))
    ice_mpg = max(5.0, float(ice_mpg))
    gas_price_per_gal = max(0.5, float(gas_price_per_gal))
    electricity_kwh_cost = max(0.01, float(electricity_kwh_cost))
    ev_kwh_per_100_miles = max(5.0, float(ev_kwh_per_100_miles))
    ev_base_msrp = max(5000.0, float(ev_base_msrp))
    ice_base_msrp = max(5000.0, float(ice_base_msrp))

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
        name="Gasoline ICE Baseline",
        line=dict(color="#71717a", width=2.5, dash="dash"),
        marker=dict(size=7, color="#a1a1aa")
    ))
    fig.add_trace(go.Scatter(
        x=timeline, y=cumulative_ev,
        mode="lines+markers",
        name="Electric Vehicle (EV)",
        line=dict(color="#de1e14", width=3),
        marker=dict(size=8, color="#de1e14")
    ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#141417",
        title=dict(
            text="<span style='font-family: TTMussels, sans-serif; letter-spacing: 0.05em; font-weight: 700; color: #ffffff;'>CUMULATIVE LIFECYCLE COST PROJECTION (USD)</span>",
            x=0.01,
            y=0.96,
            font=dict(size=13, color="#ffffff")
        ),
        font=dict(
            family="'NeueHaasGrotesk', 'Helvetica Neue', Arial, sans-serif",
            color="#a1a1aa",
            size=12
        ),
        xaxis=dict(
            title="OWNERSHIP HORIZON (YEARS)",
            gridcolor="#222228",
            zerolinecolor="#2e2e38",
            linecolor="#2c2c34",
            tickfont=dict(family="'MaisonNeueMono', monospace", size=11, color="#8e8e98")
        ),
        yaxis=dict(
            title="CUMULATIVE EXPENDITURE ($ USD)",
            gridcolor="#222228",
            zerolinecolor="#2e2e38",
            linecolor="#2c2c34",
            tickfont=dict(family="'MaisonNeueMono', monospace", size=11, color="#8e8e98")
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(family="'MaisonNeueMono', monospace", size=11, color="#d4d4d8"),
            bgcolor="rgba(22, 22, 26, 0.7)",
            bordercolor="#27272f",
            borderwidth=1
        ),
        hoverlabel=dict(
            bgcolor="#18181d",
            bordercolor="#3d3f47",
            font=dict(family="'MaisonNeueMono', monospace", size=12, color="#ffffff")
        ),
        margin=dict(l=40, r=20, t=50, b=40)
    )

    return {
        "comparison_df": comparison_df,
        "fig": fig,
        "net_savings": round(five_year_savings, 2),
        "co2_saved_tons": round(total_co2_saved_metric_tons, 2),
        "annual_fuel_savings": round(annual_ice_fuel - annual_ev_electric, 2),
        "annual_maint_savings": round(annual_ice_maint - annual_ev_maint, 2)
    }
