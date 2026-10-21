"""Flow mensal (fatia MOV): download .7z → bronze Parquet.

Prefect/Airflow entram depois; a lógica de negócio fica nesta função.
"""

from __future__ import annotations

from pathlib import Path

from src.extract import (
    bronze_partition,
    check_extracted_files,
    download_caged,
    unpack_archive,
)
from src.load import txt_to_bronze_parquet


def _primeiro_txt(arquivos: list[Path]) -> Path:
    for path in arquivos:
        if path.is_file() and path.suffix.lower() in {".txt", ".csv"}:
            return path
    raise FileNotFoundError("Nenhum .txt/.csv extraído do arquivo CAGED.")


def caged_monthly_flow(
    competencia: str,
    *,
    tipo: str = "MOV",
    overwrite: bool = False,
) -> Path:
    """Baixa um mês e materializa o Parquet bronze particionado."""
    tipo = tipo.upper()
    pasta = bronze_partition(competencia, tipo)
    arquivo_7z = download_caged(competencia, pasta, tipo=tipo, overwrite=overwrite)
    extraidos = pasta / "extracted"
    arquivos = unpack_archive(arquivo_7z, extraidos)
    check_extracted_files(extraidos)
    txt = _primeiro_txt(arquivos)
    return txt_to_bronze_parquet(
        txt,
        competencia=competencia,
        tipo=tipo,
        arquivo_origem=arquivo_7z,
        overwrite=overwrite,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("uso: python -m src.flows.caged_pipeline AAAAMM")
    print(caged_monthly_flow(sys.argv[1]))
