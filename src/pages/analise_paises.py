# src/pages/analise_paises.py

import streamlit as st
from src.data import world_bank
from src.plots import viz

def render():
    st.title("📊 Comparative Analysis between EU Countries")

    # Load data
    df = world_bank.load_lpi_data()

    # Sidebar filters
    st.sidebar.header("🎛️ Analysis Filters")

    countries = sorted(df['Country'].unique())
    selected_countries = st.sidebar.multiselect(
        "Select one or more countries",
        countries,
        default=countries[:3]
    )

    indicators = [
        'LPI Aggregate', 'Customs', 'Infrastructure',
        'International Shipments', 'Logistics Quality and Competence',
        'Tracking and Tracing', 'Timeliness'
    ]
    selected_indicator = st.sidebar.selectbox("Select an indicator", indicators)

    # Validation for country selection
    if not selected_countries:
        st.warning("🔔 Please select at least one country to continue the analysis.")
        return

    # Filter data
    df_filtered = df[df['Country'].isin(selected_countries)]

    if df_filtered.empty:
        st.error("❌ No data available for the selected countries.")
        return

    # Time evolution chart
    st.subheader(f"📈 Evolution of the **{selected_indicator}** Indicator Over the Years")
    try:
        fig = viz.plot_comparative_indicator(df_filtered, selected_countries, selected_indicator)
        st.pyplot(fig)
    except ValueError as e:
        st.error(f"Error generating chart: {e}")

    # Data table
    st.markdown("---")
    st.subheader("📄 Summary Data Table")
    display_cols = ['Country', 'Year', selected_indicator]
    st.dataframe(
        df_filtered[display_cols].sort_values(by=[selected_indicator, 'Year'], ascending=[False, False]),
        use_container_width=True
    )
