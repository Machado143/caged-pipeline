# Arquitetura

Pipeline medallion para microdados do **Novo CAGED**.

```
FTP MTE (CAGEDMOVYYYYMM.7z)
    → extract (download, py7zr, checks)
    → data/bronze/ano=AAAA/mes=MM/tipo=MOV/  (.7z + parquet varchar)
    → dbt (staging tipado → intermediate → marts)
    → data/warehouse/caged.duckdb
    → app Streamlit
```

A camada gold (`data/gold/`) fica reservada a exports; o arquivo DuckDB vive em `data/warehouse/` para não misturar warehouse com marts.

Orquestração desta fatia: função Python em `src/flows/caged_pipeline.py`. Prefect fica como extra (`pip install -e ".[orch]"`) na próxima etapa.
