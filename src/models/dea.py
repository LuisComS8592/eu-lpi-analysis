# src/models/dea.py

import numpy as np
import pandas as pd
from scipy.optimize import linprog
from sklearn.preprocessing import MinMaxScaler
import logging

logger = logging.getLogger(__name__)

def bod_model(data: pd.DataFrame, alpha: float = 0.015, beta: float = 1.000, linprog_method: str = "highs") -> pd.Series:
    """
    Calcula a eficiência dos DMUs pelo modelo DEA BoD (Benefit of the Doubt) com restrições nos pesos.

    Parâmetros:
    -----------
    data : pd.DataFrame
        DataFrame contendo os outputs (subindicadores) de cada DMU (país). Índice deve ser os nomes dos países.
    alpha : float, opcional
        Limite inferior para os pesos dos critérios (default=0.015).
    beta : float, opcional
        Limite superior para os pesos dos critérios (default=0.97).
    linprog_method : str, opcional
        Método usado pelo scipy.optimize.linprog (default='highs').

    Retorna:
    --------
    pd.Series
        Eficiência BoDw de cada DMU, indexada pelos nomes dos países.
    """
    if data.isnull().values.any():
        raise ValueError("O DataFrame contém valores ausentes.")
    if not np.issubdtype(data.values.dtype, np.number):
        raise TypeError("Todos os valores devem ser numéricos.")

    if alpha < 0 or beta > 1 or alpha >= beta:
        raise ValueError("Parâmetros alpha e beta devem satisfazer 0 <= alpha < beta <= 1.")

    # Verifica se o índice é adequado (ex: strings)
    if not all(isinstance(x, str) for x in data.index):
        logger.warning("Índice do DataFrame não parece conter nomes dos países como strings.")

    scaler = MinMaxScaler()
    # Verifica se colunas têm variação para evitar erro MinMaxScaler
    if np.any(data.nunique() <= 1):
        logger.warning("Uma ou mais colunas possuem valores constantes; normalização pode ser afetada.")

    outputs = scaler.fit_transform(data.values)
    n, m = outputs.shape
    scores = []

    # Restrição soma dos pesos = 1 (pesos somam 1, pesos entre alpha e beta)
    a_eq = np.ones((1, m))
    b_eq = np.array([1])

    # Limites dos pesos
    bounds = [(alpha, beta) for _ in range(m)]

    # Pré-cálculo das restrições A_ub, b_ub - mesma para todas as DMUs
    A_ub = outputs
    b_ub = np.ones(n)

    for j in range(n):
        c = -outputs[j]  # Maximizar outputs[j] · weights -> minimizar -outputs[j] · weights

        res = linprog(
            c=c,
            A_ub=A_ub,
            b_ub=b_ub,
            A_eq=a_eq,
            b_eq=b_eq,
            bounds=bounds,
            method=linprog_method,
        )

        if res.success:
            score = -res.fun
            # Forçar score entre 1e-6 e 1 - 1e-6 para evitar extremos
            score = min(max(score, 1e-6), 1 - 1e-6)
        else:
            logger.warning(f"Otimização falhou para {data.index[j]}: {res.message}")
            logger.debug(f"País: {data.index[j]}")
            logger.debug(f"Outputs normalizados: {outputs[j]}")
            score = np.nan

        scores.append(score)

    return pd.Series(scores, index=data.index, name="BoD Score")
