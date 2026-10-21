"""Carga bronze: TXT → Parquet via DuckDB."""

from src.load.bronze import txt_to_bronze_parquet

__all__ = ["txt_to_bronze_parquet"]
