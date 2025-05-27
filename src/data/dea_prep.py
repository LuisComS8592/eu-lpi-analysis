# src/data/dea_prep.py

import pandas as pd
from src.data import world_bank

DEA_INPUTS = [
    "Customs",
    "Infrastructure",
    "International Shipments",
    "Logistics Quality and Competence",
    "Tracking and Tracing",
    "Timeliness"
]

DEA_OUTPUT = ["LPI Aggregate"]

def prepare_dea_data(year: int, source: str = "local") -> pd.DataFrame:
    """
    Prepara os dados do LPI para análise DEA para um ano específico.

    Carrega os dados do LPI (local ou remoto), filtra pelo ano e seleciona as colunas
    necessárias para DEA, removendo linhas com dados faltantes.

    Args:
        year (int): Ano para o qual os dados serão preparados.
        source (str, opcional): Fonte dos dados, 'local' ou 'remote'. Default é 'local'.

    Returns:
        pd.DataFrame: DataFrame contendo as colunas 'Country', inputs e output, sem dados faltantes.

    Raises:
        ValueError: Se colunas necessárias estiverem ausentes no DataFrame.
        ValueError: Se não houver dados para o ano especificado.
    """
    df = world_bank.load_lpi_data(source=source)
    
    if year not in df["Year"].unique():
        raise ValueError(f"Ano {year} não encontrado nos dados disponíveis.")

    df_year = df[df["Year"] == year].copy()

    required_columns = ["Country"] + DEA_INPUTS + DEA_OUTPUT
    missing = [col for col in required_columns if col not in df_year.columns]
    if missing:
        raise ValueError(f"Colunas ausentes nos dados para o ano {year}: {missing}")

    # Remove linhas com valores faltantes nas colunas essenciais
    df_dea = df_year[required_columns].dropna().reset_index(drop=True)

    if df_dea.empty:
        raise ValueError(f"Não há dados completos para DEA no ano {year} após remoção de valores faltantes.")

    return df_dea
