# app.py

import streamlit as st
from src.pages import (
    comparacao_metodos, avaliacao_topsis, analise_envoltoria,
    subindicadores, analise_paises,
    analises_estatisticas, mapa_interativo, home
)

# Este script principal carrega a aplicação Streamlit.
# Cada página da aplicação está modularizada no diretório src/pages
# e deve conter uma função 'render()' responsável pela interface de cada aba.

def main():
    # Configuração da página Streamlit
    st.set_page_config(
        page_title="Avaliação do Desempenho Logístico na União Europeia",
        page_icon="🚚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.sidebar.title("🚦 Navegação")

    pages = {
        "Página Inicial": home.render,
        "Análises Estatísticas": analises_estatisticas.render,
        "Subindicadores por País": subindicadores.render,
        "Análise dos Países": analise_paises.render,
        "Mapa Interativo": mapa_interativo.render,
        "Análise Envoltória de Dados (DEA)": analise_envoltoria.render,
        "TOPSIS": avaliacao_topsis.render,
        "Comparação de Métodos": comparacao_metodos.render
    }

    page = st.sidebar.radio("Ir para", list(pages.keys()))

    try:
        pages[page]()
    except Exception as e:
        st.error(f"Ocorreu um erro ao carregar a página '{page}'.")
        st.exception(e)

if __name__ == "__main__":
    main()
