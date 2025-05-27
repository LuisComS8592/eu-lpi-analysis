# src/pages/avaliacao_topsis.py

import streamlit as st
from src.data import world_bank
from src.models import topsis
import pandas as pd
import plotly.express as px
from src.utils.helpers import SUBINDICATORS

def render():
    st.title("📌 Análise Multicritério - Método TOPSIS")

    st.markdown(
        """
        Esta análise utiliza o método TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)
        para ranquear os países da União Europeia com base nos subindicadores do LPI.
        """
    )

    df = world_bank.load_lpi_data()
    anos_disponiveis = sorted(df["Year"].unique(), reverse=True)

    ano = st.selectbox("Selecione o ano para análise TOPSIS", anos_disponiveis)

    df_ano = df[df["Year"] == ano].copy()

    criterios = SUBINDICATORS

    # Validar dados ausentes
    df_ano = df_ano.dropna(subset=criterios)
    if df_ano.empty:
        st.warning(f"Não há dados suficientes para análise TOPSIS no ano {ano}.")
        return

    pesos = [1 / len(criterios)] * len(criterios)  # pesos iguais

    with st.spinner("Calculando ranking TOPSIS..."):
        ranking = topsis.topsis(df_ano, criterios, pesos)

    st.subheader(f"Ranking TOPSIS ({ano})")
    st.dataframe(ranking.style.format({"TOPSIS Score": "{:.4f}"}), use_container_width=True)

    fig = px.bar(
        ranking.sort_values("TOPSIS Score", ascending=False),
        x="Country",
        y="TOPSIS Score",
        color="TOPSIS Score",
        color_continuous_scale="Blues",
        title=f"Ranking dos Países (TOPSIS) - {ano}"
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
