# src/pages/analise_envoltoria.py

import streamlit as st
import pandas as pd
from src.data import world_bank
from src.models import dea
from src.plots import viz

def render():
    st.title("📈 Logistics Efficiency - BoD Model")

    st.markdown(
        """
        This analysis uses the BoD (Benefit of the Doubt) model with constraints to assess the logistics efficiency 
        of European Union countries, based on LPI sub-indicators. The model allows each country to choose the 
        most favorable weights within established limits, reflecting its specific logistics specialization.
        """
    )

    # Data loading
    df = world_bank.load_lpi_data()
    anos_disponiveis = sorted(df["Year"].unique(), reverse=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        ano_selecionado = st.selectbox(
            "Select a year for BoD analysis",
            anos_disponiveis,
            index=0
        )
    with col2:
        mostrar_grafico = st.checkbox("Show chart", value=True)

    if ano_selecionado is None:
        st.warning("Please select a year to proceed.")
        return

    outputs = [
        "Customs",
        "Infrastructure",
        "International Shipments",
        "Logistics Quality and Competence",
        "Tracking and Tracing",
        "Timeliness"
    ]

    with st.spinner("Calculating BoD efficiency for the selected year..."):
        df_ano = df[df["Year"] == ano_selecionado].copy()
        df_ano = df_ano.dropna(subset=outputs)

        if df_ano.empty:
            st.warning("Insufficient data for the selected year after filtering.")
            return

        dados = df_ano[outputs]
        dados.index = df_ano["Country"]

        # Apply the BoD model
        scores = dea.bod_model(dados)

        results_df = pd.DataFrame({
            "Country": scores.index,
            "BoD Score": scores.values,
            "Year": ano_selecionado
        })

    st.markdown(f"### BoD Model Results for the year: {ano_selecionado}")
    st.dataframe(results_df.style.format({"BoD Score": "{:.4f}"}), use_container_width=True)

    if mostrar_grafico:
        # Prepare data for plotting
        plot_df = results_df.rename(columns={"BoD Score": "DEA Efficiency"})
        fig = viz.plot_dea_efficiency(plot_df)
        st.plotly_chart(fig, use_container_width=True)
