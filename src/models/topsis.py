# src/models/topsis.py

import pandas as pd
import numpy as np

def topsis(df: pd.DataFrame, criterios: list[str], pesos: list[float]) -> pd.DataFrame:
    """
    Aplica o método TOPSIS para ranquear alternativas com base em critérios de benefício.

    Parâmetros:
    -----------
    df : pd.DataFrame
        DataFrame contendo pelo menos uma coluna "Country" e as colunas dos critérios.
    criterios : list[str]
        Lista com os nomes das colunas que serão usados como critérios.
    pesos : list[float]
        Pesos relativos a cada critério (serão normalizados automaticamente).

    Retorna:
    --------
    pd.DataFrame
        DataFrame com colunas: "Country", "TOPSIS Score" e "Ranking", ordenado pelo ranking.
    """
    if "Country" not in df.columns:
        raise ValueError("O DataFrame deve conter uma coluna chamada 'Country'.")

    if len(criterios) != len(pesos):
        raise ValueError("O número de critérios deve ser igual ao número de pesos.")

    if any(p < 0 for p in pesos):
        raise ValueError("Os pesos não podem conter valores negativos.")

    if df[criterios].isnull().values.any():
        raise ValueError("Há valores ausentes nos critérios fornecidos.")

    # Etapa 1: Matriz de decisão (alternativas x critérios)
    matriz_decisao = df[criterios].astype(float).values

    # Etapa 2: Normalização da matriz pelo método Euclidiano (norma L2)
    norm_fatores = np.linalg.norm(matriz_decisao, axis=0)
    norm_fatores = np.where(norm_fatores == 0, 1, norm_fatores)  # evitar divisão por zero
    matriz_normalizada = matriz_decisao / norm_fatores

    # Etapa 3: Normalização dos pesos
    pesos_arr = np.array(pesos, dtype=float)
    soma_pesos = pesos_arr.sum()
    if soma_pesos == 0:
        raise ValueError("A soma dos pesos não pode ser zero.")
    pesos_norm = pesos_arr / soma_pesos

    # Etapa 4: Construção da matriz ponderada
    matriz_ponderada = matriz_normalizada * pesos_norm

    # Etapa 5: Identificação das soluções ideal (máximo) e anti-ideal (mínimo)
    ideal = np.max(matriz_ponderada, axis=0)
    anti_ideal = np.min(matriz_ponderada, axis=0)

    # Etapa 6: Cálculo das distâncias euclidianas para o ideal e anti-ideal
    dist_ideal = np.linalg.norm(matriz_ponderada - ideal, axis=1)
    dist_anti_ideal = np.linalg.norm(matriz_ponderada - anti_ideal, axis=1)

    # Etapa 7: Cálculo do score TOPSIS
    scores = dist_anti_ideal / (dist_ideal + dist_anti_ideal)

    # Construção do DataFrame resultado com ranking coerente
    resultado = df[["Country"]].copy()
    resultado["TOPSIS Score"] = scores
    resultado["Ranking"] = resultado["TOPSIS Score"].rank(ascending=False, method="min").astype(int)

    return resultado.sort_values("Ranking").reset_index(drop=True)
