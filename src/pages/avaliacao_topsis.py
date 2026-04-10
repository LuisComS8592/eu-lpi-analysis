# src/pages/avaliacao_topsis.py

import streamlit as st
from src.data import world_bank
from src.models import topsis
import pandas as pd
import plotly.express as px
from src.utils.helpers import SUBINDICATORS

def render():
    st.title("📌 Multicriteria Analysis - TOPSIS Method")

    st.markdown(
        """
        This analysis utilizes the TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) 
        method to rank European Union countries based on LPI sub-indicators. 
        It evaluates performance by measuring the distance of each country to the 
        theoretical ideal (best observed values) and the negative-ideal solutions.
        """
    )

    df = world_bank.load_lpi_data()
    anos_disponiveis = sorted(df["Year"].unique(), reverse=True)

    ano = st.selectbox("Select the year for TOPSIS analysis", anos_disponiveis)

    df_ano = df[df["Year"] == ano].copy()

    criterios = SUBINDICATORS

    # Validate missing data
    df_ano = df_ano.dropna(subset=criterios)
    if df_ano.empty:
        st.warning(f"Insufficient data for TOPSIS analysis in the year {ano}.")
        return

    pesos = [1 / len(criterios)] * len(criterios)  # equal weights

    with st.spinner("Calculating TOPSIS ranking..."):
        ranking = topsis.topsis(df_ano, criterios, pesos)

    st.subheader(f"TOPSIS Ranking ({ano})")
    st.dataframe(ranking.style.format({"TOPSIS Score": "{:.4f}"}), use_container_width=True)

    fig = px.bar(
        ranking.sort_values("TOPSIS Score", ascending=False),
        x="Country",
        y="TOPSIS Score",
        color="TOPSIS Score",
        color_continuous_scale="RdYlGn",
        title=f"Country Ranking (TOPSIS) - {ano}",
        labels={"TOPSIS Score": "Performance Score", "Country": "Country"}
    )
    fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
    st.plotly_chart(fig, use_container_width=True)
