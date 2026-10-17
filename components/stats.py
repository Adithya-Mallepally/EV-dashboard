"""
components/stats.py
───────────────────
Top KPI telemetry cards rendered in dark minimalist automotive design system.
Zero emojis, zero icons. Clean typography using Maison Neue Mono and Neue Haas Grotesk.
"""

import streamlit as st


def render_kpis(df):
    """Render top KPI metric cards from filtered DataFrame in minimalist automotive aesthetic."""
    total = len(df)
    avg_range = df["Electric Range"].mean() if total > 0 else 0
    top_make = df["Make"].value_counts().idxmax() if total > 0 else "N/A"

    bev_count = len(df[df["Electric Vehicle Type"].str.startswith("Battery")])
    bev_pct = (bev_count / total * 100) if total > 0 else 0

    kpis = [
        {
            "label": "TOTAL VEHICLES",
            "value": f"{total:,}",
            "meta": "REGISTERED FLEET POPULATION"
        },
        {
            "label": "AVG ELECTRIC RANGE",
            "value": f"{avg_range:.0f} MI",
            "meta": "EPA ESTIMATED MEAN"
        },
        {
            "label": "LEADING MANUFACTURER",
            "value": top_make.upper(),
            "meta": "MAX FLEET CONCENTRATION"
        },
        {
            "label": "BEV MARKET SHARE",
            "value": f"{bev_pct:.1f}%",
            "meta": "PURE BATTERY ELECTRIC"
        }
    ]

    cols = st.columns(4)
    for col, kpi in zip(cols, kpis):
        with col:
            card_html = f"""
            <div class="telemetry-card">
                <div class="telemetry-card-label">{kpi['label']}</div>
                <div class="telemetry-card-value">{kpi['value']}</div>
                <div class="telemetry-card-meta">{kpi['meta']}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
