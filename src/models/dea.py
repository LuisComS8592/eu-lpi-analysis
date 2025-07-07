# src/models/dea.py

import numpy as np
import pandas as pd
from scipy.optimize import linprog
from sklearn.preprocessing import MinMaxScaler
import logging
from typing import Union

logger = logging.getLogger(__name__)

def bod_model(
    data: pd.DataFrame, 
    normalize_data: bool = False,
    normalize_weights: bool = False,
    alpha: float = 0.0, 
    beta: float = None,
    return_weights: bool = False,
    linprog_method: str = "highs"
) -> Union[pd.Series, tuple[pd.Series, pd.DataFrame]]:
    """
    Calcula a eficiência dos DMUs pelo modelo DEA BoD (Benefit of the Doubt).

    Parâmetros:
    -----------
    data : pd.DataFrame
        DataFrame com os outputs (subindicadores) de cada DMU (país).
    normalize_data : bool, opcional
        Se True, aplica a normalização MinMaxScaler aos dados (default=False).
    normalize_weights : bool, opcional
        Se True, força a soma dos pesos a ser igual a 1 (default=False).
    alpha : float, opcional
        Limite inferior para os pesos (default=0.0).
    beta : float, opcional
        Limite superior para os pesos (default=None).
    return_weights : bool, opcional
        Se True, retorna uma tupla (scores, weights). 
        Se False, retorna apenas a série de scores para manter a compatibilidade (default=False).
    linprog_method : str, opcional
        Método para o scipy.optimize.linprog (default='highs').

    Retorna:
    --------
    Union[pd.Series, tuple[pd.Series, pd.DataFrame]]
        - Se `return_weights=False`: pd.Series com os scores de eficiência.
        - Se `return_weights=True`: Tupla (pd.Series com scores, pd.DataFrame com pesos).
    """
    # --- Validação de Entradas ---
    if data.isnull().values.any():
        raise ValueError("O DataFrame contém valores ausentes.")
    if not np.issubdtype(data.values.dtype, np.number):
        raise TypeError("Todos os valores no DataFrame devem ser numéricos.")
    if not all(isinstance(x, str) for x in data.index):
        logger.warning("O índice do DataFrame não parece conter nomes de países como strings.")

    # --- Pré-processamento dos Dados (Condicional) ---
    if normalize_data:
        if np.any(data.nunique() <= 1):
            logger.warning("Uma ou mais colunas possuem valores constantes; a normalização pode ser afetada.")
        scaler = MinMaxScaler()
        outputs = scaler.fit_transform(data)
    else:
        outputs = data.values

    n, m = outputs.shape
    scores = []
    all_weights = []
    
    # --- Validação dos Pesos ---
    if normalize_weights:
        if beta is None or beta > 1.0:
            beta = 1.0
        if alpha < 0 or alpha >= beta:
            raise ValueError("Com normalize_weights=True, os parâmetros devem satisfazer 0 <= alpha < beta <= 1.")
        if m * alpha > 1:
            raise ValueError(f"Conflito de restrições: a soma mínima dos pesos ({m*alpha}) é > 1.")
        if m * beta < 1:
            raise ValueError(f"Conflito de restrições: a soma máxima dos pesos ({m*beta}) é < 1.")
    else:
        if beta is not None and alpha >= beta:
            raise ValueError("O limite inferior (alpha) deve ser menor que o superior (beta).")

    # --- Definição das Restrições da Programação Linear ---
    bounds = [(alpha, beta) for _ in range(m)]
    A_ub = outputs
    b_ub = np.ones(n)
    A_eq, b_eq = (np.ones((1, m)), np.array([1])) if normalize_weights else (None, None)

    # --- Otimização para cada DMU ---
    for j in range(n):
        c = -outputs[j]

        res = linprog(c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method=linprog_method)

        if res.success:
            score = -res.fun
            weights = res.x
        else:
            logger.warning(f"A otimização falhou para {data.index[j]}: {res.message}")
            score = np.nan
            weights = np.full(m, np.nan)

        scores.append(score)
        all_weights.append(weights)
    
    # --- Formatação do Resultado Final ---
    final_scores = pd.Series(scores, index=data.index, name="BoD_Score")
    final_weights = pd.DataFrame(all_weights, index=data.index, columns=data.columns)

    if return_weights:
        return final_scores, final_weights
    else:
        return final_scores
