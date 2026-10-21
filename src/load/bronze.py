"""Bronze: TXT/CSV → Parquet via DuckDB (streaming, tudo varchar)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import duckdb

from src.config import CSV_DELIM, CSV_ENCODINGS
from src.extract.competencia import parse_competencia
from src.extract.download import bronze_partition
from src.extract.hashing import sha256_file


def _posix(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/").replace("'", "''")


def _read_csv_sql(origem: Path, encoding: str) -> str:
    return (
        f"read_csv('{_posix(origem)}', "
        f"delim='{CSV_DELIM}', "
        "header=true, "
        f"encoding='{encoding}', "
        "all_varchar=true, "
        "sample_size=-1)"
    )


def txt_to_bronze_parquet(
    origem: Path,
    *,
    competencia: str,
    tipo: str = "MOV",
    arquivo_origem: Path | None = None,
    destino: Path | None = None,
    overwrite: bool = False,
) -> Path:
    """Grava Parquet particionado por ano/mês/tipo com metadados de ingestão."""
    tipo = tipo.upper()
    pasta = bronze_partition(competencia, tipo)
    pasta.mkdir(parents=True, exist_ok=True)
    parquet = destino or (pasta / "caged.parquet")
    if parquet.exists() and not overwrite:
        return parquet

    fonte = arquivo_origem or origem
    digest = sha256_file(fonte)
    carga = datetime.now(UTC).isoformat()
    parse_competencia(competencia)

    last_error: Exception | None = None
    con = duckdb.connect(database=":memory:")
    try:
        for encoding in CSV_ENCODINGS:
            sql = f"""
            COPY (
              SELECT
                src.*,
                '{_posix(fonte)}' AS _arquivo_origem,
                '{digest}' AS _hash_sha256,
                '{carga}' AS _data_carga,
                '{tipo}' AS _tipo_arquivo,
                '{competencia}' AS _competencia_arquivo
              FROM {_read_csv_sql(origem, encoding)} AS src
            ) TO '{_posix(parquet)}' (FORMAT PARQUET, COMPRESSION ZSTD)
            """
            try:
                con.execute(sql)
                return parquet
            except Exception as exc:  # noqa: BLE001 — fallback de encoding
                last_error = exc
                if parquet.exists():
                    parquet.unlink()
        raise RuntimeError(
            f"Falha ao ler {origem} com encodings {CSV_ENCODINGS}: {last_error}"
        ) from last_error
    finally:
        con.close()
