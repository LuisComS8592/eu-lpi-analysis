# src/pages/analise_envoltoria.py

import streamlit as st
import pandas as pd
from src.data import world_bank
from src.models import dea
from src.plots import viz

def render():
    st.title("📈 Eficiência Logística - Modelo BoD")

    st.markdown(
        """
        Esta análise utiliza o modelo BoD (Benefit of the Doubt) com restrições para avaliar a eficiência logística dos países da União Europeia,
        com base nos subindicadores do LPI. O modelo permite que cada país escolha os pesos mais favoráveis, dentro de limites estabelecidos,
        refletindo sua especialização logística.
        """
    )

    # Carregamento dos dados
    df = world_bank.load_lpi_data()
    anos_disponiveis = sorted(df["Year"].unique(), reverse=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        ano_selecionado = st.selectbox(
            "Selecione um ano para análise BoD",
            anos_disponiveis,
            index=0
        )
    with col2:
        mostrar_grafico = st.checkbox("Mostrar gráfico", value=True)

    if ano_selecionado is None:
        st.warning("Selecione um ano para prosseguir.")
        return

    outputs = [
        "Customs",
        "Infrastructure",
        "International Shipments",
        "Logistics Quality and Competence",
        "Tracking and Tracing",
        "Timeliness"
    ]

    with st.spinner("Calculando eficiência BoD para o ano selecionado..."):
        df_ano = df[df["Year"] == ano_selecionado].copy()
        df_ano = df_ano.dropna(subset=outputs)

        if df_ano.empty:
            st.warning("Não há dados suficientes para o ano selecionado após filtragem.")
            return

        dados = df_ano[outputs]
        dados.index = df_ano["Country"]

        # Aplicar o modelo BoD
        scores = dea.bod_model(dados)

        results_df = pd.DataFrame({
            "Country": scores.index,
            "BoD Score": scores.values,
            "Year": ano_selecionado
        })

    st.markdown(f"### Resultados do Modelo BoD para o ano: {ano_selecionado}")
    st.dataframe(results_df.style.format({"BoD Score": "{:.4f}"}), use_container_width=True)

    if mostrar_grafico:
        # Preparar dados para plotagem
        plot_df = results_df.rename(columns={"BoD Score": "DEA Efficiency"})
        fig = viz.plot_dea_efficiency(plot_df)
        st.plotly_chart(fig, use_container_width=True)
