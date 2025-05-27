# src/pages/analises_estatisticas.py

import streamlit as st
from src.data import world_bank
from src.analysis import stat_analysis
from src.plots import viz
import matplotlib.pyplot as plt

def render():
    st.title("Análises Estatísticas do Desempenho Logístico")

    # Carregar dados
    df = world_bank.load_lpi_data()

    indicators = [
        'LPI Aggregate', 'Customs', 'Infrastructure', 'International Shipments',
        'Logistics Quality and Competence', 'Tracking and Tracing', 'Timeliness'
    ]

    # Estatísticas descritivas globais
    st.header("📊 Estatísticas Descritivas Globais")
    stats_global = stat_analysis.descriptive_stats_global(df, indicators)

    col1, col2 = st.columns(2)
    col1.metric("Média LPI Aggregate", f"{stats_global.loc['mean', 'LPI Aggregate']:.3f}")
    col2.metric("Desvio Padrão", f"{stats_global.loc['std', 'LPI Aggregate']:.3f}")

    st.dataframe(stats_global.style.format("{:.3f}"))

    st.markdown("---")

    # Histograma
    st.header("📈 Histograma do LPI Aggregate")
    fig_hist = viz.plot_histogram(df, 'LPI Aggregate')
    st.pyplot(fig_hist)
    plt.close(fig_hist)

    st.markdown("---")

    # Boxplot por ano
    st.header("📦 Boxplot do LPI Aggregate por Ano")
    fig_box = viz.plot_boxplot_by_year(df, 'LPI Aggregate')
    st.pyplot(fig_box)
    plt.close(fig_box)

    st.markdown("---")

    # Heatmap de correlação
    st.header("🧪 Matriz de Correlação dos Indicadores")
    fig_heatmap = viz.plot_correlation_heatmap_seaborn(df, indicators)
    st.pyplot(fig_heatmap)
    plt.close(fig_heatmap)
    st.caption("Valores próximos de 1 indicam forte correlação positiva; próximos de -1, correlação negativa.")

    st.markdown("---")

    # Relação entre indicadores selecionáveis
    st.header("🔍 Relação entre Indicadores")
    col1, col2 = st.columns(2)
    x_indicator = col1.selectbox("Indicador no eixo X", indicators, index=2)
    y_indicator = col2.selectbox("Indicador no eixo Y", indicators, index=0)

    if x_indicator != y_indicator:
        fig_scatter = viz.plot_scatter_regression(df, x_indicator, y_indicator)
        st.pyplot(fig_scatter)
        plt.close(fig_scatter)

        st.subheader("📐 Teste de Correlação de Pearson")
        stats = viz.pearson_correlation_test(df, x_indicator, y_indicator)
        st.write(f"**Correlação de Pearson entre {x_indicator} e {y_indicator}**: `{stats['correlation']:.3f}`")
        st.write(f"**Valor-p**: `{stats['p_value']:.4f}`")

        if stats['p_value'] < 0.05:
            st.success("A correlação é estatisticamente significativa, ou seja, há evidência de uma relação linear entre os indicadores.")
        else:
            st.warning("A correlação não é estatisticamente significativa, indicando que não há evidência de relação linear entre os indicadores.")
    else:
        st.info("Por favor, selecione dois indicadores diferentes.")
