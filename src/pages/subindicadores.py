# src/pages/subindicadores.py

import streamlit as st
from src.data import world_bank
from src.plots import viz

def render():
    st.title("📊 Pontos Fortes e Fracos por Subindicadores")

    # Carregar dados
    df = world_bank.load_lpi_data()

    # Filtros laterais
    st.sidebar.header("🎛️ Filtros")
    selected_country = st.sidebar.selectbox("Selecione um país", sorted(df["Country"].unique()))

    all_years = sorted(df["Year"].unique(), reverse=True)
    selected_years = st.sidebar.multiselect(
        "Selecione um ou mais anos",
        all_years,
        default=[all_years[0]]
    )

    # Verificações básicas
    if not selected_years:
        st.warning("🔔 Selecione ao menos um ano para visualizar os subindicadores.")
        return

    st.markdown(f"### 📌 Desempenho do país **{selected_country}** por Subindicadores")

    # Subindicadores a analisar
    subindicators = [
        "Customs",
        "Infrastructure",
        "International Shipments",
        "Logistics Quality and Competence",
        "Tracking and Tracing",
        "Timeliness"
    ]

    # Radar e tabela
    try:
        fig, tabela = viz.plot_radar_subindicators(df, selected_country, selected_years, subindicators)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### 📄 Tabela de Valores dos Subindicadores")
        st.dataframe(tabela, use_container_width=True)
    except ValueError as e:
        st.error(f"❌ Erro ao gerar visualização: {e}")
