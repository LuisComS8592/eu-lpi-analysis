# src/pages/home.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from src.data import world_bank

# Application home page with an overview of LPI in the EU

def render():
    # Custom Style
    st.markdown(
        """
        <style>
        .main > div.block-container {
            max-width: 900px;
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1 { font-weight: 700; }
        .subtitle {
            font-size: 20px;
            line-height: 1.5;
            margin-bottom: 2rem;
        }
        .kpi {
            font-size: 1.3rem;
            font-weight: 600;
        }
        .nav-item {
            font-size: 1.05rem;
            margin-bottom: 12px;
            padding-left: 0.25rem;
        }
        .nav-emoji {
            font-weight: 700;
            margin-right: 0.5rem;
        }
        .footer {
            font-size: 12px;
            margin-top: 3rem;
            border-top: 1px solid var(--border-color);
            padding-top: 12px;
            text-align: center;
        }
        a { font-weight: 600; text-decoration: none; }
        a:hover { text-decoration: underline; }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Title and description
    st.markdown("# 🚛 Logistics Performance Assessment in the European Union")
    st.markdown(
        '<div class="subtitle">Interactive system for analyzing the logistics performance of European Union countries, based on the World Bank\'s Logistics Performance Index (LPI).</div>',
        unsafe_allow_html=True
    )

    # Load data
    df = world_bank.load_lpi_data()
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    # Main KPIs
    ultimo_ano = int(df['Year'].max())
    media_lpi = df[df['Year'] == ultimo_ano]['LPI Aggregate'].mean()
    num_paises = df['Country'].nunique()

    col1, col2, col3 = st.columns([1.8, 1.2, 1])
    col1.markdown(f'<div class="kpi">📅 <b>Most Recent Year:</b> {ultimo_ano}</div>', unsafe_allow_html=True)
    col2.metric(label="Average Aggregate LPI (EU)", value=f"{media_lpi:.2f}")
    col3.metric(label="EU Countries", value=num_paises)

    st.markdown("---")

    # Annual LPI Average Chart
    sns.set_theme(style="whitegrid", palette="muted")
    media_ano = df.groupby('Year')['LPI Aggregate'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 4.5))
    sns.lineplot(x='Year', y='LPI Aggregate', data=media_ano, marker='o', ax=ax, color="#0B4C5F", linewidth=2)
    ax.set_title('Evolution of Average Aggregate LPI in the European Union', fontsize=16, fontweight='bold', color='#0B4C5F')
    ax.set_xlabel('Year', fontsize=13)
    ax.set_ylabel('Average LPI', fontsize=13)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=40)

    # st.pyplot(fig)
    st.plotly_chart(px.line(media_ano, x='Year', y='LPI Aggregate', 
                            labels={'LPI Aggregate': 'Average LPI', 'Year': 'Year'},
                            title='Evolution of Average Aggregate LPI in the EU'))

    st.markdown("---")

    # Quick Navigation
    st.subheader("Quick Navigation")
    nav_col1, nav_col2 = st.columns(2)

    nav_col1.markdown('<div class="nav-item"><span class="nav-emoji">📊</span><b>Statistical Analysis</b> — Explore indicators and trends.</div>', unsafe_allow_html=True)
    nav_col1.markdown('<div class="nav-item"><span class="nav-emoji">🇪🇺</span><b>Country Analysis</b> — Detailed comparison between EU countries.</div>', unsafe_allow_html=True)
    nav_col2.markdown('<div class="nav-item"><span class="nav-emoji">📈</span><b>Sub-indicators by Country</b> — Visualize LPI components.</div>', unsafe_allow_html=True)
    nav_col2.markdown('<div class="nav-item"><span class="nav-emoji">🗺️</span><b>Interactive Map</b> — Geographic data analysis.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Footer
    st.markdown(
        """
        <div class="footer">
        Project developed by <b>Luis</b> | Supervisor: Clara Bento Vaz | March to June 2025<br>
        Data extracted from the <a href="https://lpi.worldbank.org/" target="_blank">World Bank - Logistics Performance Index (LPI)</a>
        </div>
        """, unsafe_allow_html=True
    )
