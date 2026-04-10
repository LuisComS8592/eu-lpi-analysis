# src/pages/subindicadores.py

import streamlit as st
from src.data import world_bank
from src.plots import viz

def render():
    st.title("📊 Strengths and Weaknesses by Sub-indicators")

    # Load data
    df = world_bank.load_lpi_data()

    # Sidebar filters
    st.sidebar.header("🎛️ Filters")
    selected_country = st.sidebar.selectbox("Select a country", sorted(df["Country"].unique()))

    all_years = sorted(df["Year"].unique(), reverse=True)
    selected_years = st.sidebar.multiselect(
        "Select one or more years",
        all_years,
        default=[all_years[0]]
    )

    # Basic validations
    if not selected_years:
        st.warning("🔔 Please select at least one year to view the sub-indicators.")
        return

    st.markdown(f"### 📌 Performance of **{selected_country}** by Sub-indicators")

    # Sub-indicators to analyze
    subindicators = [
        "Customs",
        "Infrastructure",
        "International Shipments",
        "Logistics Quality and Competence",
        "Tracking and Tracing",
        "Timeliness"
    ]

    # Radar chart and table
    try:
        # Assuming viz.plot_radar_subindicators handles title/labels via its logic
        # If not, ensure the internal labels in viz.py are also in English.
        fig, table = viz.plot_radar_subindicators(df, selected_country, selected_years, subindicators)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📄 Table of Sub-indicator Values")
        st.dataframe(table, use_container_width=True)
    except ValueError as e:
        st.error(f"❌ Error generating visualization: {e}")
