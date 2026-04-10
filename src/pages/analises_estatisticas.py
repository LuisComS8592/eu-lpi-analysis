# src/pages/analises_estatisticas.py

import streamlit as st
from src.data import world_bank
from src.analysis import stat_analysis
from src.plots import viz
import matplotlib.pyplot as plt

def render():
    st.title("Statistical Analysis of Logistics Performance")

    # Load data
    df = world_bank.load_lpi_data()

    indicators = [
        'LPI Aggregate', 'Customs', 'Infrastructure', 'International Shipments',
        'Logistics Quality and Competence', 'Tracking and Tracing', 'Timeliness'
    ]

    # Global descriptive statistics
    st.header("📊 Global Descriptive Statistics")
    stats_global = stat_analysis.descriptive_stats_global(df, indicators)

    col1, col2 = st.columns(2)
    col1.metric("Average Aggregate LPI", f"{stats_global.loc['mean', 'LPI Aggregate']:.3f}")
    col2.metric("Standard Deviation", f"{stats_global.loc['std', 'LPI Aggregate']:.3f}")

    st.dataframe(stats_global.style.format("{:.3f}"))

    st.markdown("---")

    # Histogram
    st.header("📈 Histogram of Aggregate LPI")
    fig_hist = viz.plot_histogram(df, 'LPI Aggregate')
    st.pyplot(fig_hist)
    plt.close(fig_hist)

    st.markdown("---")

    # Boxplot by year
    st.header("📦 Boxplot of Aggregate LPI by Year")
    fig_box = viz.plot_boxplot_by_year(df, 'LPI Aggregate')
    st.pyplot(fig_box)
    plt.close(fig_box)

    st.markdown("---")

    # Correlation heatmap
    st.header("🧪 Correlation Matrix of Indicators")
    fig_heatmap = viz.plot_correlation_heatmap_seaborn(df, indicators)
    st.pyplot(fig_heatmap)
    plt.close(fig_heatmap)
    st.caption("Values close to 1 indicate a strong positive correlation; values close to -1 indicate a negative correlation.")

    st.markdown("---")

    # Relationship between selectable indicators
    st.header("🔍 Relationship between Indicators")
    col1, col2 = st.columns(2)
    x_indicator = col1.selectbox("Indicator for X-axis", indicators, index=2)
    y_indicator = col2.selectbox("Indicator for Y-axis", indicators, index=0)

    if x_indicator != y_indicator:
        fig_scatter = viz.plot_scatter_regression(df, x_indicator, y_indicator)
        st.pyplot(fig_scatter)
        plt.close(fig_scatter)

        st.subheader("📐 Pearson Correlation Test")
        stats = viz.pearson_correlation_test(df, x_indicator, y_indicator)
        st.write(f"**Pearson Correlation between {x_indicator} and {y_indicator}**: `{stats['correlation']:.3f}`")
        st.write(f"**p-value**: `{stats['p_value']:.4f}`")

        if stats['p_value'] < 0.05:
            st.success("The correlation is statistically significant, meaning there is evidence of a linear relationship between the indicators.")
        else:
            st.warning("The correlation is not statistically significant, indicating no evidence of a linear relationship between the indicators.")
    else:
        st.info("Please select two different indicators.")
