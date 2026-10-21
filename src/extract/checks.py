"""Checagens de integridade após extração."""

from __future__ import annotations

from pathlib import Path


def check_extracted_files(diretorio: Path, *, min_bytes: int = 1) -> list[Path]:
    """Garante que há arquivos extraídos não vazios."""
    arquivos = [p for p in diretorio.rglob("*") if p.is_file()]
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo extraído em {diretorio}")
    vazios = [p for p in arquivos if p.stat().st_size < min_bytes]
    if vazios:
        nomes = ", ".join(str(p) for p in vazios)
        raise ValueError(f"Arquivos vazios ou corrompidos: {nomes}")
    return arquivos
