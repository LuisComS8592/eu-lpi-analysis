# src/pages/mapa_interativo.py

import streamlit as st
import pandas as pd
from src.data import world_bank
from src.plots.viz import plot_europe_map
import plotly.express as px

def render():
    st.title("🗺️ Interactive Logistics Performance Map")

    # Load data
    df = world_bank.load_lpi_data()

    # --- Sidebar filters ---
    st.sidebar.header("Filters")

    anos_disponiveis = sorted(df["Year"].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Select year", anos_disponiveis, index=0)

    comparar_anos = st.sidebar.checkbox("Compare two years?")
    selected_year_2 = None
    if comparar_anos:
        # Avoid choosing the same year for comparison
        selected_year_2 = st.sidebar.selectbox(
            "Select second year",
            [ano for ano in anos_disponiveis if ano != selected_year],
            index=0
        )

    indicadores = [
        'LPI Aggregate', 'Customs', 'Infrastructure',
        'International Shipments', 'Logistics Quality and Competence',
        'Tracking and Tracing', 'Timeliness'
    ]
    selected_indicator = st.sidebar.selectbox("Select indicator for map", indicadores)

    paises = sorted(df['Country'].unique())
    selected_countries = st.sidebar.multiselect("Select countries (optional)", paises, default=paises)

    # Filter data based on selection
    if selected_countries:
        df = df[df['Country'].isin(selected_countries)]

    st.markdown(f"### Interactive Map: **{selected_indicator}**")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Map for the first year
        fig = plot_europe_map(df, selected_year, selected_indicator)
        st.plotly_chart(fig, use_container_width=True)

        # Map for second year, if selected
        if comparar_anos and selected_year_2:
            st.markdown(f"### Map for Year {selected_year_2}")
            fig2 = plot_europe_map(df, selected_year_2, selected_indicator)
            st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown(f"### Indicator Summary Statistics ({selected_year})")

        df_ano = df[df["Year"] == selected_year]

        if not df_ano.empty:
            media = df_ano[selected_indicator].mean()
            minimo = df_ano[selected_indicator].min()
            maximo = df_ano[selected_indicator].max()

            stats_df = pd.DataFrame({
                "Statistic": ["Mean", "Minimum", "Maximum"],
                "Value": [media, minimo, maximo]
            })

            st.table(stats_df.style.format({"Value": "{:.3f}"}))

            fig_stats = px.bar(
                stats_df,
                x="Statistic",
                y="Value",
                color="Statistic",
                text=stats_df["Value"].map(lambda x: f"{x:.3f}"),
                labels={"Value": selected_indicator, "Statistic": "Statistic"},
                height=250,
                template="plotly_white"
            )
            st.plotly_chart(fig_stats, use_container_width=True)
        else:
            st.info("No data available for the selected year.")

        st.markdown("---")

        st.markdown(f"### Detailed Data - Year {selected_year}")
        df_detalhes = df[df["Year"] == selected_year].reset_index(drop=True)
        st.dataframe(df_detalhes, use_container_width=True)

        csv = df_detalhes.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download data as CSV",
            data=csv,
            file_name=f'lpi_data_{selected_year}.csv',
            mime='text/csv',
        )
