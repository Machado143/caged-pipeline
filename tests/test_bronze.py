from pathlib import Path

import duckdb

from src.load.bronze import txt_to_bronze_parquet

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "CAGEDMOV202301.txt"


def test_bronze_tudo_varchar_e_metadados(tmp_path: Path):
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
    cols = con.execute(
        f"describe select * from read_parquet('{destino.as_posix()}')"
    ).fetchall()
    tipos = {row[0]: row[1] for row in cols}
    assert tipos["competênciamov"].upper().startswith("VARCHAR")
    assert tipos["salário"].upper().startswith("VARCHAR")
    assert tipos["_hash_sha256"].upper().startswith("VARCHAR")
    n = con.execute(
        f"select count(*) from read_parquet('{destino.as_posix()}')"
    ).fetchone()[0]
    assert n == 6
    ingestao = con.execute(
        f"""
        select _tipo_arquivo, _competencia_arquivo
        from read_parquet('{destino.as_posix()}')
        limit 1
        """
    ).fetchone()
    assert ingestao == ("MOV", "202301")
