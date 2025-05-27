# src/pages/mapa_interativo.py

import streamlit as st
import pandas as pd
from src.data import world_bank
from src.plots.viz import plot_europe_map
import plotly.express as px

def render():
    st.title("🗺️ Mapa Interativo do Desempenho Logístico")

    # Carregar dados
    df = world_bank.load_lpi_data()

    # --- Sidebar filtros ---
    st.sidebar.header("Filtros")

    anos_disponiveis = sorted(df["Year"].unique(), reverse=True)
    selected_year = st.sidebar.selectbox("Selecione o ano", anos_disponiveis, index=0)

    comparar_anos = st.sidebar.checkbox("Comparar dois anos?")
    selected_year_2 = None
    if comparar_anos:
        # Evitar escolher o mesmo ano para comparação
        selected_year_2 = st.sidebar.selectbox(
            "Selecione o segundo ano",
            [ano for ano in anos_disponiveis if ano != selected_year],
            index=0
        )

    indicadores = [
        'LPI Aggregate', 'Customs', 'Infrastructure',
        'International Shipments', 'Logistics Quality and Competence',
        'Tracking and Tracing', 'Timeliness'
    ]
    selected_indicator = st.sidebar.selectbox("Selecione o indicador para o mapa", indicadores)

    paises = sorted(df['Country'].unique())
    selected_countries = st.sidebar.multiselect("Selecione países (opcional)", paises, default=paises)

    # Filtrar dados conforme seleção
    if selected_countries:
        df = df[df['Country'].isin(selected_countries)]

    st.markdown(f"### Mapa Interativo do Indicador **{selected_indicator}**")

    col1, col2 = st.columns([2, 1])

    with col1:
        # Mapa para o primeiro ano
        fig = plot_europe_map(df, selected_year, selected_indicator)
        st.plotly_chart(fig, use_container_width=True)

        # Mapa para segundo ano, se selecionado
        if comparar_anos and selected_year_2:
            st.markdown(f"### Mapa para o ano {selected_year_2}")
            fig2 = plot_europe_map(df, selected_year_2, selected_indicator)
            st.plotly_chart(fig2, use_container_width=True)

    with col2:
        st.markdown(f"### Estatísticas Resumo do Indicador ({selected_year})")

        df_ano = df[df["Year"] == selected_year]

        if not df_ano.empty:
            media = df_ano[selected_indicator].mean()
            minimo = df_ano[selected_indicator].min()
            maximo = df_ano[selected_indicator].max()

            stats_df = pd.DataFrame({
                "Estatística": ["Média", "Mínimo", "Máximo"],
                "Valor": [media, minimo, maximo]
            })

            st.table(stats_df.style.format({"Valor": "{:.3f}"}))

            fig_stats = px.bar(
                stats_df,
                x="Estatística",
                y="Valor",
                color="Estatística",
                text=stats_df["Valor"].map(lambda x: f"{x:.3f}"),
                labels={"Valor": selected_indicator},
                height=250
            )
            st.plotly_chart(fig_stats, use_container_width=True)
        else:
            st.info("Sem dados para o ano selecionado.")

        st.markdown("---")

        st.markdown(f"### Dados Detalhados - Ano {selected_year}")
        df_detalhes = df[df["Year"] == selected_year].reset_index(drop=True)
        st.dataframe(df_detalhes, use_container_width=True)

        csv = df_detalhes.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar dados em CSV",
            data=csv,
            file_name=f'dados_lpi_{selected_year}.csv',
            mime='text/csv',
        )
