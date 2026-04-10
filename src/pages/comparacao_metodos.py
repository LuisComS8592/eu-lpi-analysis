# src/pages/comparacao_metodos.py

import streamlit as st
import pandas as pd
from src.data import world_bank
from src.models import dea, topsis
from src.utils.helpers import SUBINDICATORS
from src.plots import viz

def render():
    st.title("📊 Country Ranking Comparison")

    st.markdown(
        """
        This page presents a comparative analysis of the original LPI rankings (World Bank)
        with the rankings derived via DEA (BoD) and TOPSIS.
        
        In addition to tables and charts, we calculate correlations between rankings and highlight
        convergences and divergences between the methodologies.
        """
    )

    df = world_bank.load_lpi_data()
    anos_disponiveis = sorted(df["Year"].unique(), reverse=True)
    ano = st.selectbox("Select year for analysis", anos_disponiveis)
    df_ano = df[df["Year"] == ano].copy()

    subindicadores = SUBINDICATORS
    df_ano = df_ano.dropna(subset=subindicadores + ["LPI Aggregate"])
    if df_ano.empty:
        st.warning(f"Insufficient data for the year {ano} after filtering.")
        return

    # Ensure sub-indicators are numeric
    for col in subindicadores:
        df_ano[col] = pd.to_numeric(df_ano[col], errors="coerce")
    df_ano = df_ano.dropna(subset=subindicadores + ["Country"])
    if df_ano.empty:
        st.warning("Insufficient data after converting sub-indicators to numeric values.")
        return

    # DEA (Benefit of the Doubt)
    inputs = df_ano[subindicadores]
    dea_result = dea.bod_model(inputs)
    dea_ranking = pd.DataFrame({
        "Country": df_ano["Country"].values,
        "Efficiency Score": dea_result.values
    })
    dea_ranking["DEA Rank"] = dea_ranking["Efficiency Score"].rank(ascending=False, method="min").astype(int)

    # TOPSIS
    n_criterios = int(len(subindicadores))
    pesos = [1.0 / n_criterios] * n_criterios
    topsis_result = topsis.topsis(df_ano[["Country"] + subindicadores], subindicadores, pesos)
    topsis_result = topsis_result.rename(columns={"Ranking": "TOPSIS Rank"})

    # World Bank Ranking
    df_ano["WB Rank"] = df_ano["LPI Aggregate"].rank(ascending=False, method="min").astype(int)

    # Combine rankings
    comparativo = df_ano[["Country", "WB Rank"]].merge(
        dea_ranking[["Country", "DEA Rank"]], on="Country", how="inner"
    ).merge(
        topsis_result[["Country", "TOPSIS Rank"]], on="Country", how="inner"
    )

    st.subheader(f"Ranking Comparison Table - Year {ano}")
    st.dataframe(comparativo.set_index("Country"), use_container_width=True)

    # Spearman Correlations
    st.subheader("Spearman Rank Correlation")
    corr_matrix = comparativo[["WB Rank", "DEA Rank", "TOPSIS Rank"]].corr(method='spearman')
    st.dataframe(corr_matrix.style.format("{:.2f}"), use_container_width=True)

    fig_corr = viz.plot_correlation_heatmap_plotly(corr_matrix)
    st.plotly_chart(fig_corr, use_container_width=True)

    # Scatter Plots
    st.subheader("Ranking Scatter Analysis")
    comparativo_clean = comparativo.dropna(subset=["WB Rank", "DEA Rank", "TOPSIS Rank"])

    fig = viz.plot_scatter_ranking(comparativo_clean, "WB Rank", "DEA Rank", "World Bank Rank", "DEA Rank")
    st.plotly_chart(fig, use_container_width=True)

    fig = viz.plot_scatter_ranking(comparativo_clean, "WB Rank", "TOPSIS Rank", "World Bank Rank", "TOPSIS Rank")
    st.plotly_chart(fig, use_container_width=True)

    fig = viz.plot_scatter_ranking(comparativo_clean, "DEA Rank", "TOPSIS Rank", "DEA Rank", "TOPSIS Rank")
    st.plotly_chart(fig, use_container_width=True)

    # Highlights: Convergences and Divergences
    st.subheader("Highlights - Convergence and Divergence")
    threshold = 3

    comparativo["DEA vs WB"] = (comparativo["DEA Rank"] - comparativo["WB Rank"]).abs()
    comparativo["TOPSIS vs WB"] = (comparativo["TOPSIS Rank"] - comparativo["WB Rank"]).abs()

    convergentes = comparativo[
        (comparativo["DEA vs WB"] <= threshold) & 
        (comparativo["TOPSIS vs WB"] <= threshold)
    ]

    divergentes = comparativo[
        (comparativo["DEA vs WB"] > threshold) |
        (comparativo["TOPSIS vs WB"] > threshold)
    ]

    st.markdown(f"**Countries with convergent rankings (difference ≤ {threshold} positions across all methods):** {len(convergentes)}")
    st.dataframe(convergentes.set_index("Country")[["WB Rank", "DEA Rank", "TOPSIS Rank"]], use_container_width=True)

    st.markdown(f"**Countries with significant divergences (difference > {threshold} positions in at least one method):** {len(divergentes)}")
    st.dataframe(divergentes.set_index("Country")[["WB Rank", "DEA Rank", "TOPSIS Rank"]], use_container_width=True)
