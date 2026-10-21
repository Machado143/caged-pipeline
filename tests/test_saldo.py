from pathlib import Path

import duckdb

from src.load.bronze import txt_to_bronze_parquet

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "CAGEDMOV202301.txt"


def test_saldo_e_soma_nao_contagem(tmp_path: Path):
    destino = tmp_path / "caged.parquet"
    txt_to_bronze_parquet(
        FIXTURE,
        competencia="202301",
        tipo="MOV",
        arquivo_origem=FIXTURE,
        destino=destino,
        overwrite=True,
    )
    con = duckdb.connect(database=":memory:")
    saldo, linhas = con.execute(
        f"""
        select
          sum(try_cast("saldomovimentação" as integer)) as saldo,
          count(*) as linhas
        from read_parquet('{destino.as_posix()}')
        """
    ).fetchone()
    assert linhas == 6
    assert saldo == 2
