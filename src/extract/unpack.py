"""Descompactação dos arquivos CAGED (.7z oficial; .zip por compatibilidade)."""

from __future__ import annotations

import zipfile
from pathlib import Path

import py7zr


def unpack_archive(arquivo: Path, destino: Path) -> list[Path]:
    """Extrai .7z ou .zip e retorna a lista de arquivos gerados."""
    destino.mkdir(parents=True, exist_ok=True)
    sufixo = arquivo.suffix.lower()
    if sufixo == ".7z" or py7zr.is_7zfile(arquivo):
        with py7zr.SevenZipFile(arquivo, mode="r") as archive:
            nomes = archive.getnames()
            archive.extractall(path=destino)
        return [destino / name for name in nomes]
    if zipfile.is_zipfile(arquivo):
        with zipfile.ZipFile(arquivo) as zf:
            zf.extractall(destino)
            return [destino / name for name in zf.namelist()]
    raise ValueError(f"Arquivo inválido (esperado .7z ou .zip): {arquivo}")
