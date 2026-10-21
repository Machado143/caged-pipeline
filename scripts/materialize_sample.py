"""Gera o Parquet bronze de amostra usado no CI, testes e dashboard."""

from __future__ import annotations

from pathlib import Path

from src.config import WAREHOUSE_DIR
from src.load import txt_to_bronze_parquet

FIXTURE = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "CAGEDMOV202301.txt"


def materialize_sample(*, overwrite: bool = True) -> Path:
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)
    return txt_to_bronze_parquet(
        FIXTURE,
        competencia="202301",
        tipo="MOV",
        arquivo_origem=FIXTURE,
        overwrite=overwrite,
    )


if __name__ == "__main__":
    print(materialize_sample())
