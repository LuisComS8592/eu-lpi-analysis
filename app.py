# app.py

import streamlit as st
from src.pages import (
    comparacao_metodos, avaliacao_topsis, analise_envoltoria,
    subindicadores, analise_paises,
    analises_estatisticas, mapa_interativo, home
)

# This main script loads the Streamlit application.
# Each page of the application is modularized in the src/pages directory
# and must contain a 'render()' function responsible for the interface of each tab.

def main():
    # Streamlit page configuration
    st.set_page_config(
        page_title="Logistics Performance Assessment in the European Union",
        page_icon="🚚",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.sidebar.title("🚦 Navigation")

    # Map page names to their respective render functions
    pages = {
        "Home Page": home.render,
        "Statistical Analysis": analises_estatisticas.render,
        "Sub-indicators by Country": subindicadores.render,
        "Country Analysis": analise_paises.render,
        "Interactive Map": mapa_interativo.render,
        "Data Envelopment Analysis (DEA)": analise_envoltoria.render,
        "TOPSIS": avaliacao_topsis.render,
        "Methods Comparison": comparacao_metodos.render
    }

    # Navigation menu
    page = st.sidebar.radio("Go to", list(pages.keys()))

    try:
        # Render the selected page
        pages[page]()
    except Exception as e:
        st.error(f"An error occurred while loading the page '{page}'.")
        st.exception(e)

if __name__ == "__main__":
    main()
