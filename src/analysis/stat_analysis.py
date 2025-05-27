# src/analysis/stat_analysis.py

import os
import logging
from typing import List

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

sns.set(style="whitegrid")

RESULTS_DIR = "results"

def validate_columns(df: pd.DataFrame, columns: List[str]) -> None:
    """Valida se todas as colunas estão presentes no DataFrame."""
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Colunas ausentes no DataFrame: {missing}")

def export_dataframe_to_csv(df: pd.DataFrame, filepath: str) -> None:
    """
    Exporta DataFrame para CSV, criando diretório se não existir.

    Args:
        df (pd.DataFrame): DataFrame a ser exportado.
        filepath (str): Caminho do arquivo CSV.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=True)
    logging.info(f"DataFrame exportado para: {filepath}")

def descriptive_stats_global(df: pd.DataFrame, indicators: List[str]) -> pd.DataFrame:
    """
    Retorna estatísticas descritivas globais dos indicadores.

    Args:
        df (pd.DataFrame): DataFrame com os dados.
        indicators (List[str]): Lista de indicadores (colunas).

    Returns:
        pd.DataFrame: Estatísticas descritivas.
    """
    validate_columns(df, indicators)
    return df[indicators].describe()

def descriptive_stats_by_year(df: pd.DataFrame, indicators: List[str]) -> pd.DataFrame:
    """
    Retorna estatísticas descritivas agrupadas por ano.

    Args:
        df (pd.DataFrame): DataFrame com os dados.
        indicators (List[str]): Lista de indicadores.

    Returns:
        pd.DataFrame: Estatísticas descritivas agrupadas por ano.
    """
    validate_columns(df, ['Year'] + indicators)
    return df.groupby('Year')[indicators].describe()

def mean_by_country(df: pd.DataFrame, indicators: List[str], sort_by: str = 'LPI Aggregate') -> pd.DataFrame:
    """
    Calcula a média dos indicadores por país, ordenando pelo indicador especificado.

    Args:
        df (pd.DataFrame): DataFrame com os dados.
        indicators (List[str]): Lista de indicadores.
        sort_by (str): Indicador para ordenar o resultado.

    Returns:
        pd.DataFrame: Médias por país ordenadas.
    """
    validate_columns(df, ['Country'] + indicators)
    if sort_by not in indicators:
        raise ValueError(f"Indicador para ordenação '{sort_by}' não está na lista de indicadores.")
    grouped = df.groupby('Country')[indicators].mean()
    return grouped.sort_values(by=sort_by, ascending=False)

def correlation_matrix(df: pd.DataFrame, indicators: List[str]) -> pd.DataFrame:
    """
    Calcula matriz de correlação entre indicadores.

    Args:
        df (pd.DataFrame): DataFrame com dados.
        indicators (List[str]): Lista de indicadores.

    Returns:
        pd.DataFrame: Matriz de correlação.
    """
    validate_columns(df, indicators)
    return df[indicators].corr()

def pearson_correlation_test(df: pd.DataFrame, x_indicator: str, y_indicator: str) -> None:
    """
    Realiza teste de correlação de Pearson entre dois indicadores, com impressão do resultado.

    Args:
        df (pd.DataFrame): DataFrame com dados.
        x_indicator (str): Indicador X.
        y_indicator (str): Indicador Y.
    """
    validate_columns(df, [x_indicator, y_indicator])
    clean_df = df[[x_indicator, y_indicator]].dropna()
    corr, p_value = pearsonr(clean_df[x_indicator], clean_df[y_indicator])
    logging.info(f"Correlação de Pearson entre '{x_indicator}' e '{y_indicator}': {corr:.3f}")
    logging.info(f"Valor-p: {p_value:.4f}")
    if p_value < 0.05:
        logging.info("Correlação estatisticamente significativa ao nível de 5%")
    else:
        logging.info("Correlação NÃO é estatisticamente significativa ao nível de 5%")

def main():
    """
    Função principal para executar a análise estatística descritiva do LPI, salvar resultados
    e gerar gráficos exemplares.
    """
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    from src.data import world_bank
    from src.plots import viz

    indicators = [
        'LPI Aggregate', 'Customs', 'Infrastructure', 'International Shipments',
        'Logistics Quality and Competence', 'Tracking and Tracing', 'Timeliness'
    ]

    df = world_bank.load_lpi_data()

    logging.info("Calculando estatísticas globais...")
    stats_global = descriptive_stats_global(df, indicators)
    logging.info("\n%s", stats_global)
    export_dataframe_to_csv(stats_global, os.path.join(RESULTS_DIR, "stats_global.csv"))

    logging.info("Calculando estatísticas por ano...")
    stats_year = descriptive_stats_by_year(df, indicators)
    logging.info("\n%s", stats_year)
    export_dataframe_to_csv(stats_year, os.path.join(RESULTS_DIR, "stats_by_year.csv"))

    logging.info("Calculando média por país...")
    mean_country = mean_by_country(df, indicators)
    logging.info("\n%s", mean_country)
    export_dataframe_to_csv(mean_country, os.path.join(RESULTS_DIR, "mean_by_country.csv"))

    logging.info("Gerando visualizações...")

    fig1 = viz.plot_comparative_indicator(df, ['Germany', 'France', 'Italy'], 'LPI Aggregate')
    fig1.show()
    plt.close(fig1)

    fig2 = viz.plot_europe_map(df, year=2018, indicator='LPI Aggregate')
    fig2.show()
    plt.close(fig2)

    pearson_correlation_test(df, 'Infrastructure', 'LPI Aggregate')

if __name__ == "__main__":
    main()
