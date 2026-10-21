"""Download dos microdados Novo CAGED no FTP do MTE/PDET."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

from src.config import ARQUIVO_PREFIXO, BRONZE_DIR, FTP_BASE_DIR, FTP_HOST
from src.extract.competencia import parse_competencia


def caged_ftp_url(competencia: str, tipo: str = "MOV") -> str:
    """URL FTP oficial: .../NOVO CAGED/<AAAA>/<AAAAMM>/CAGEDMOV<AAAAMM>.7z"""
    tipo = tipo.upper()
    if tipo not in ARQUIVO_PREFIXO:
        raise ValueError(f"Tipo inválido: {tipo}. Use MOV, FOR ou EXC.")
    ano, _mes = parse_competencia(competencia)
    nome = f"{ARQUIVO_PREFIXO[tipo]}{competencia}.7z"
    caminho = f"{FTP_BASE_DIR}/{ano}/{competencia}/{nome}"
    return f"ftp://{FTP_HOST}{quote(caminho, safe='/')}"


def bronze_partition(competencia: str, tipo: str = "MOV") -> Path:
    ano, mes = parse_competencia(competencia)
    return BRONZE_DIR / f"ano={ano}" / f"mes={mes}" / f"tipo={tipo.upper()}"


def download_caged(
    competencia: str,
    destino: Path | None = None,
    *,
    tipo: str = "MOV",
    overwrite: bool = False,
    timeout: int = 900,
) -> Path:
    """Baixa o .7z da competência para a partição bronze.

    O FTP do MTE costuma aceitar só conexões no Brasil.
    """
    tipo = tipo.upper()
    pasta = Path(destino) if destino is not None else bronze_partition(competencia, tipo)
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / f"{ARQUIVO_PREFIXO[tipo]}{competencia}.7z"
    if arquivo.exists() and not overwrite:
        return arquivo

    url = caged_ftp_url(competencia, tipo)
    tmp = arquivo.with_suffix(".7z.partial")
    try:
        with urlopen(url, timeout=timeout) as resp, tmp.open("wb") as fh:
            while chunk := resp.read(1024 * 1024):
                fh.write(chunk)
        tmp.replace(arquivo)
    except Exception:
        if tmp.exists():
            tmp.unlink()
        raise
    return arquivo
