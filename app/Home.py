"""Dashboard Streamlit: saldo CAGED por UF e seção CNAE."""

from __future__ import annotations

import duckdb
import pandas as pd
import streamlit as st

from src.config import ROOT, WAREHOUSE_PATH

st.set_page_config(page_title="CAGED Pipeline", layout="wide")
st.title("CAGED — saldo de empregos")
st.caption("Saldo = soma de `saldomovimentação` (+1/−1), não contagem de linhas.")

_SQL_PARQUET = """
select
  try_cast("competênciamov" as integer) as competencia,
  try_cast(uf as integer) as uf,
  "seção" as secao,
  sum(try_cast("saldomovimentação" as integer)) as saldo,
  sum(
    case when try_cast("saldomovimentação" as integer) = 1 then 1 else 0 end
  ) as admissoes,
  sum(
    case when try_cast("saldomovimentação" as integer) = -1 then 1 else 0 end
  ) as desligamentos,
  count(*) as qtd_movimentacoes
from read_parquet('{parquet}')
group by 1, 2, 3
"""


def _carregar_fato() -> pd.DataFrame:
    if WAREHOUSE_PATH.exists():
        con = duckdb.connect(str(WAREHOUSE_PATH), read_only=True)
        try:
            return con.execute("select * from marts.fct_saldo_mensal").df()
        except duckdb.Error:
            pass
        finally:
            con.close()

    parquet = ROOT / "data" / "bronze" / "ano=2023" / "mes=01" / "tipo=MOV" / "caged.parquet"
    if not parquet.exists():
        from scripts.materialize_sample import materialize_sample

        parquet = materialize_sample()

    con = duckdb.connect(database=":memory:")
    return con.execute(_SQL_PARQUET.format(parquet=parquet.as_posix())).df()


df = _carregar_fato()
if df.empty:
    st.warning(
        "Nenhuma mart encontrada. Rode `python scripts/materialize_sample.py` "
        "e `make dbt-build`."
    )
    st.stop()

total_saldo = int(df["saldo"].sum())
c1, c2, c3 = st.columns(3)
c1.metric("Saldo líquido", f"{total_saldo:+d}")
c2.metric("Admissões", int(df["admissoes"].sum()))
c3.metric("Desligamentos", int(df["desligamentos"].sum()))

por_secao = df.groupby("secao", as_index=False)["saldo"].sum()
st.subheader("Saldo por seção CNAE")
st.bar_chart(por_secao, x="secao", y="saldo")

st.subheader("Detalhe")
st.dataframe(df.sort_values(["competencia", "uf", "secao"]), use_container_width=True)
