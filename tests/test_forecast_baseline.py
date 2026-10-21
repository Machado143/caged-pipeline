import pandas as pd

from src.forecast.baseline import naive_forecast


def test_naive_forecast_repete_ultimo_valor():
    serie = pd.Series([10, 20, 30], name="saldo")
    prev = naive_forecast(serie, horizonte=2)
    assert list(prev) == [30, 30]
