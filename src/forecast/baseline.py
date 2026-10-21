"""Baseline ingênuo de saldo de empregos."""

from __future__ import annotations

import pandas as pd


def naive_forecast(serie: pd.Series, horizonte: int = 3) -> pd.Series:
    """Repete o último valor observado pelo horizonte informado."""
    if serie.empty:
        raise ValueError("Série vazia.")
    ultimo = serie.iloc[-1]
    idx = pd.RangeIndex(horizonte, name=serie.index.name)
    return pd.Series([ultimo] * horizonte, index=idx, name=serie.name)
