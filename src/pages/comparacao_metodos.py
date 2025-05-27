# src/pages/comparacao_metodos.py

import streamlit as st
import pandas as pd
from src.data import world_bank
from src.models import dea, topsis
from src.utils.helpers import SUBINDICATORS
from src.plots import viz

def render():
    st.title("📊 Comparação dos Rankings dos Países")

    st.markdown(
        """
        Esta página apresenta uma análise comparativa dos rankings do LPI original (World Bank)
        com os rankings derivados por DEA e TOPSIS.
        
        Além de tabelas e gráficos, calculamos correlações entre rankings e destacamos
        convergências e divergências entre os métodos.
        """
    )

    df = world_bank.load_lpi_data()
    anos_disponiveis = sorted(df["Year"].unique(), reverse=True)
    ano = st.selectbox("Selecione o ano para análise", anos_disponiveis)
    df_ano = df[df["Year"] == ano].copy()

    subindicadores = SUBINDICATORS
    df_ano = df_ano.dropna(subset=subindicadores + ["LPI Aggregate"])
    if df_ano.empty:
        st.warning(f"Não há dados suficientes para o ano {ano} após filtragem.")
        return

    # Garantir que os subindicadores são numéricos
    for col in subindicadores:
        df_ano[col] = pd.to_numeric(df_ano[col], errors="coerce")
    df_ano = df_ano.dropna(subset=subindicadores + ["Country"])
    if df_ano.empty:
        st.warning("Dados insuficientes após a conversão dos subindicadores para valores numéricos.")
        return

    # DEA
    inputs = df_ano[subindicadores]
    dea_result = dea.bodw_model(inputs)
    dea_ranking = pd.DataFrame({
        "Country": df_ano["Country"].values,
        "Efficiency Score": dea_result.values
    })
    dea_ranking["Ranking DEA"] = dea_ranking["Efficiency Score"].rank(ascending=False, method="min").astype(int)

    # TOPSIS
    n_criterios = int(len(subindicadores))
    pesos = [1.0 / n_criterios] * n_criterios
    topsis_result = topsis.topsis(df_ano[["Country"] + subindicadores], subindicadores, pesos)
    topsis_result = topsis_result.rename(columns={"Ranking": "Ranking TOPSIS"})

    # Ranking World Bank
    df_ano["Ranking WB"] = df_ano["LPI Aggregate"].rank(ascending=False, method="min").astype(int)

    # Combinar rankings
    comparativo = df_ano[["Country", "Ranking WB"]].merge(
        dea_ranking[["Country", "Ranking DEA"]], on="Country", how="inner"
    ).merge(
        topsis_result[["Country", "Ranking TOPSIS"]], on="Country", how="inner"
    )

    st.subheader(f"Tabela Comparativa dos Rankings - Ano {ano}")
    st.dataframe(comparativo.set_index("Country"), use_container_width=True)

    # Correlações de Spearman
    st.subheader("Correlação de Spearman entre Rankings")
    corr_matrix = comparativo[["Ranking WB", "Ranking DEA", "Ranking TOPSIS"]].corr(method='spearman')
    st.dataframe(corr_matrix.style.format("{:.2f}"), use_container_width=True)

    fig_corr = viz.plot_correlation_heatmap_plotly(corr_matrix)
    st.plotly_chart(fig_corr, use_container_width=True)

    # Gráficos de dispersão
    st.subheader("Dispersão entre Rankings")
    comparativo_clean = comparativo.dropna(subset=["Ranking WB", "Ranking DEA", "Ranking TOPSIS"])

    fig = viz.plot_scatter_ranking(comparativo_clean, "Ranking WB", "Ranking DEA", "Ranking World Bank", "Ranking DEA")
    st.plotly_chart(fig, use_container_width=True)

    fig = viz.plot_scatter_ranking(comparativo_clean, "Ranking WB", "Ranking TOPSIS", "Ranking World Bank", "Ranking TOPSIS")
    st.plotly_chart(fig, use_container_width=True)

    # Destaques de convergências/divergências
    st.subheader("Destaques - Convergências e Divergências")
    threshold = 3

    comparativo["DEA vs WB"] = (comparativo["Ranking DEA"] - comparativo["Ranking WB"]).abs()
    comparativo["TOPSIS vs WB"] = (comparativo["Ranking TOPSIS"] - comparativo["Ranking WB"]).abs()

    convergentes = comparativo[
        (comparativo["DEA vs WB"] <= threshold) & 
        (comparativo["TOPSIS vs WB"] <= threshold)
    ]

    divergentes = comparativo[
        (comparativo["DEA vs WB"] > threshold) |
        (comparativo["TOPSIS vs WB"] > threshold)
    ]

    st.markdown(f"**Países com ranking convergente (diferença ≤ {threshold} posições em todos os métodos):** {len(convergentes)}")
    st.dataframe(convergentes.set_index("Country")[["Ranking WB", "Ranking DEA", "Ranking TOPSIS"]], use_container_width=True)

    st.markdown(f"**Países com divergências significativas (diferença > {threshold} posições em ao menos um método):** {len(divergentes)}")
    st.dataframe(divergentes.set_index("Country")[["Ranking WB", "Ranking DEA", "Ranking TOPSIS"]], use_container_width=True)
