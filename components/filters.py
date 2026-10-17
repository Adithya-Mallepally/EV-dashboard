"""
components/filters.py
─────────────────────
Sidebar filter controls styled in the DeLorean design system.
Zero emojis, zero icons. Technical labels in Neue Haas Grotesk and Maison Neue Mono.
"""

import streamlit as st


def render_filters(df):
    """Render sidebar filters and return filtered DataFrame."""
    st.sidebar.markdown("""
    <div style="font-family: 'MaisonNeueMono', monospace; font-size: 11px; letter-spacing: 0.16em; color: #de1e14; text-transform: uppercase; margin-bottom: 4px;">
        TELEMETRY CONTROLS
    </div>
    <div style="font-family: 'NeueHaasGrotesk', sans-serif; font-size: 18px; font-weight: 700; letter-spacing: 0.04em; color: #ffffff; text-transform: uppercase; margin-bottom: 1rem;">
        SYSTEM FILTERS
    </div>
    """, unsafe_allow_html=True)

    # Make filter
    all_makes = sorted(df["Make"].unique().tolist())
    top5 = df["Make"].value_counts().head(5).index.tolist()
    selected_makes = st.sidebar.multiselect("Manufacturer", all_makes, default=top5)

    # EV Type filter
    ev_types = df["Electric Vehicle Type"].unique().tolist()
    selected_types = st.sidebar.multiselect("Propulsion Type", ev_types, default=ev_types)

    # Model Year slider
    min_year, max_year = int(df["Model Year"].min()), int(df["Model Year"].max())
    year_range = st.sidebar.slider("Model Year Horizon", min_year, max_year, (2016, max_year))

    # Electric Range slider
    min_range, max_range = int(df["Electric Range"].min()), int(df["Electric Range"].max())
    range_filter = st.sidebar.slider("Electric Range Threshold (Miles)", min_range, max_range, (min_range, max_range))

    # Apply filters
    filtered = df[
        df["Make"].isin(selected_makes) &
        df["Electric Vehicle Type"].isin(selected_types) &
        df["Model Year"].between(*year_range) &
        df["Electric Range"].between(*range_filter)
    ]

    st.sidebar.markdown("<hr style='border: none; border-top: 1px solid #232328; margin: 1.5rem 0;'>", unsafe_allow_html=True)
    st.sidebar.markdown(f"""
    <div style="background: #16161a; border: 1px solid #27272f; border-left: 3px solid #de1e14; padding: 12px 14px; border-radius: 2px;">
        <div style="font-family: 'MaisonNeueMono', monospace; font-size: 10px; color: #8e8e98; text-transform: uppercase; letter-spacing: 0.1em;">FILTER STATUS</div>
        <div style="font-family: 'NeueHaasGrotesk', sans-serif; font-size: 16px; font-weight: 700; color: #ffffff; margin-top: 2px;">{len(filtered):,} / {len(df):,}</div>
        <div style="font-family: 'MaisonNeueMono', monospace; font-size: 10px; color: #71717a; margin-top: 2px;">ACTIVE VEHICLES MATCHED</div>
    </div>
    """, unsafe_allow_html=True)

    return filtered
