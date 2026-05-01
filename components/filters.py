import streamlit as st

def render_filters(df):
    """Render sidebar filters and return filtered DataFrame."""
    st.sidebar.markdown("## ⚡ Filters")

    # Make filter
    all_makes = sorted(df["Make"].unique().tolist())
    top5 = df["Make"].value_counts().head(5).index.tolist()
    selected_makes = st.sidebar.multiselect("🚗 Make", all_makes, default=top5)

    # EV Type filter
    ev_types = df["Electric Vehicle Type"].unique().tolist()
    selected_types = st.sidebar.multiselect("🔋 EV Type", ev_types, default=ev_types)

    # Model Year slider
    min_year, max_year = int(df["Model Year"].min()), int(df["Model Year"].max())
    year_range = st.sidebar.slider("📅 Model Year", min_year, max_year, (2016, max_year))

    # Electric Range slider
    min_range, max_range = int(df["Electric Range"].min()), int(df["Electric Range"].max())
    range_filter = st.sidebar.slider("🛣️ Electric Range (miles)", min_range, max_range, (min_range, max_range))

    # Apply filters
    filtered = df[
        df["Make"].isin(selected_makes) &
        df["Electric Vehicle Type"].isin(selected_types) &
        df["Model Year"].between(*year_range) &
        df["Electric Range"].between(*range_filter)
    ]

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**{len(filtered):,}** vehicles match filters")

    return filtered
