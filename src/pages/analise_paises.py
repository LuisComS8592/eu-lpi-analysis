# src/pages/analise_paises.py

import streamlit as st
from src.data import world_bank
from src.plots import viz

def render():
    st.title("📊 Análise Comparativa entre Países da União Europeia")

    # Carregar dados
    df = world_bank.load_lpi_data()

    # Filtros laterais
    st.sidebar.header("🎛️ Filtros de Análise")

    countries = sorted(df['Country'].unique())
    selected_countries = st.sidebar.multiselect(
        "Selecione um ou mais países",
        countries,
        default=countries[:3]
    )

    indicators = [
        'LPI Aggregate', 'Customs', 'Infrastructure',
        'International Shipments', 'Logistics Quality and Competence',
        'Tracking and Tracing', 'Timeliness'
    ]
    selected_indicator = st.sidebar.selectbox("Selecione um indicador", indicators)

    # Validação da seleção de países
    if not selected_countries:
        st.warning("🔔 Selecione pelo menos um país para continuar a análise.")
        return

    # Filtrar dados
    df_filtered = df[df['Country'].isin(selected_countries)]

    if df_filtered.empty:
        st.error("❌ Nenhum dado disponível para os países selecionados.")
        return

    # Gráfico de evolução temporal
    st.subheader(f"📈 Evolução do Indicador **{selected_indicator}** ao Longo dos Anos")
    try:
        fig = viz.plot_comparative_indicator(df_filtered, selected_countries, selected_indicator)
        st.pyplot(fig)
    except ValueError as e:
        st.error(f"Erro ao gerar gráfico: {e}")

    # Tabela de dados
    st.markdown("---")
    st.subheader("📄 Tabela de Dados Resumidos")
    display_cols = ['Country', 'Year', selected_indicator]
    st.dataframe(
        df_filtered[display_cols].sort_values(by=[selected_indicator, 'Year'], ascending=[False, False]),
        use_container_width=True
    )
