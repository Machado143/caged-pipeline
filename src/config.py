"""Caminhos e constantes do pipeline."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
WAREHOUSE_DIR = DATA_DIR / "warehouse"
WAREHOUSE_PATH = WAREHOUSE_DIR / "caged.duckdb"

FTP_HOST = "ftp.mtps.gov.br"
FTP_BASE_DIR = "/pdet/microdados/NOVO CAGED"

ARQUIVO_PREFIXO = {
    "MOV": "CAGEDMOV",
    "FOR": "CAGEDFOR",
    "EXC": "CAGEDEXC",
}

# Oficial MTE: Novo CAGED em UTF-8, `;`, vírgula decimal.
# latin-1 entra como fallback para arquivos legados.
CSV_ENCODINGS = ("utf-8", "latin-1")
CSV_DELIM = ";"
