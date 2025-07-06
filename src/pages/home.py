# src/pages/home.py

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.data import world_bank

# Página inicial da aplicação com visão geral do LPI na UE

def render():
    # Estilo customizado
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

    # Título e descrição
    st.markdown("# 🚛 Avaliação do Desempenho Logístico na União Europeia")
    st.markdown(
        '<div class="subtitle">Sistema interativo para análise do desempenho logístico dos países da União Europeia, baseado no Índice de Desempenho Logístico (LPI) do Banco Mundial.</div>',
        unsafe_allow_html=True
    )

    # Carrega dados
    df = world_bank.load_lpi_data()
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    # KPIs principais
    ultimo_ano = int(df['Year'].max())
    media_lpi = df[df['Year'] == ultimo_ano]['LPI Aggregate'].mean()
    num_paises = df['Country'].nunique()

    col1, col2, col3 = st.columns([1.8, 1.2, 1])
    col1.markdown(f'<div class="kpi">📅 <b>Ano mais recente:</b> {ultimo_ano}</div>', unsafe_allow_html=True)
    col2.metric(label="Média LPI Agregado (UE)", value=f"{media_lpi:.2f}")
    col3.metric(label="Países da UE", value=num_paises)

    st.markdown("---")

    # Gráfico da média anual do LPI
    sns.set_theme(style="whitegrid", palette="muted")
    media_ano = df.groupby('Year')['LPI Aggregate'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 4.5))
    sns.lineplot(x='Year', y='LPI Aggregate', data=media_ano, marker='o', ax=ax, color="#0B4C5F", linewidth=2)
    ax.set_title('Evolução da Média do LPI Agregado na União Europeia', fontsize=16, fontweight='bold', color='#0B4C5F')
    ax.set_xlabel('Ano', fontsize=13)
    ax.set_ylabel('LPI Médio', fontsize=13)
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.xticks(rotation=40)

    # st.pyplot(fig)
    st.plotly_chart(px.line(media_ano, x='Year', y='LPI Aggregate'))  # alternativa interativa opcional

    st.markdown("---")

    # Navegação rápida
    st.subheader("Navegação Rápida")
    nav_col1, nav_col2 = st.columns(2)

    nav_col1.markdown('<div class="nav-item"><span class="nav-emoji">📊</span><b>Análises Estatísticas</b> — Explore indicadores e tendências.</div>', unsafe_allow_html=True)
    nav_col1.markdown('<div class="nav-item"><span class="nav-emoji">🇪🇺</span><b>Análise dos Países</b> — Comparação detalhada entre países da UE.</div>', unsafe_allow_html=True)
    nav_col2.markdown('<div class="nav-item"><span class="nav-emoji">📈</span><b>Subindicadores por País</b> — Visualize os componentes do LPI.</div>', unsafe_allow_html=True)
    nav_col2.markdown('<div class="nav-item"><span class="nav-emoji">🗺️</span><b>Mapa Interativo</b> — Análise geográfica dos dados.</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Rodapé
    st.markdown(
        """
        <div class="footer">
        Projeto desenvolvido por <b>Luis</b> | Orientadora: Clara Bento Vaz | Março a Junho de 2025<br>
        Dados extraídos do <a href="https://lpi.worldbank.org/" target="_blank">World Bank - Índice de Desempenho Logístico (LPI)</a>
        </div>
        """, unsafe_allow_html=True
    )
