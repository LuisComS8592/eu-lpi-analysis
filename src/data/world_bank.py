# src/data/world_bank.py

import pandas as pd
import os

def load_lpi_data(source: str = "local") -> pd.DataFrame:
    """
    Carrega os dados do LPI a partir de um arquivo local ou de uma fonte remota.

    Parameters:
        source (str): 'local' para carregar do CSV local, 'remote' para usar processamento externo.

    Returns:
        pd.DataFrame: DataFrame contendo os dados do LPI.
    """
    source = source.lower()
    
    if source == "local":
        path = os.path.join("data", "World_Bank_LPI.csv")
        try:
            df = pd.read_csv(path)
            if "Year" in df.columns:
                df["Year"] = pd.to_numeric(df["Year"], errors='coerce')
            return df
        except FileNotFoundError:
            raise FileNotFoundError(f"Arquivo CSV não encontrado em {path}. Verifique se ele existe.")
    
    elif source == "remote":
        try:
            from src.utils.helpers import load_remote_lpi_data
            return load_remote_lpi_data()
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar dados remotos: {e}")
    
    else:
        raise ValueError("Fonte inválida. Use 'local' ou 'remote'.")
