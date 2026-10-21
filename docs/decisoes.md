# Decisões

## Camadas medallion

Bronze: `.7z` original + Parquet **tudo varchar** (DuckDB `all_varchar=true`), particionado por `ano/mes/tipo`, com colunas de ingestão. Tipagem só no `stg_caged`.

## Warehouse

DuckDB em `data/warehouse/caged.duckdb`, não em `data/gold/`. Gold fica para tabelas exportadas.

## Encoding

Documentação do MTE (microdados Novo CAGED): UTF-8. O loader tenta UTF-8 e cai para latin-1.

## Carga

DuckDB `read_csv` + `COPY TO PARQUET` em vez de Polars, para não materializar o TXT inteiro em Python.

## Saldo

Regra de negócio: soma de `saldomovimentação` (+1/−1). Contar linhas mede movimentações, não o saldo.

## Orquestração

Função Python nesta fatia. Prefect como extra opcional (`orch`) na etapa seguinte.

## Dados versionados

Conteúdo de `data/` fora do Git. Seeds em `dbt/seeds/*.csv` explicitamente reincluídos no `.gitignore`.
