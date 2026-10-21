# caged-pipeline

Pipeline medallion dos microdados do **Novo CAGED**.

Fonte FTP (MTE/PDET):

`ftp://ftp.mtps.gov.br/pdet/microdados/NOVO CAGED/<AAAA>/<AAAAMM>/CAGEDMOV<AAAAMM>.7z`

O FTP costuma responder só a partir do Brasil. Layout oficial usa `competênciamov`, `seção`, `saldomovimentação`, `salário` (UTF-8, `;`, vírgula decimal).

## Uso rápido (amostra, sem FTP)

```bash
make install
make test
make dbt-build
make app
```

Um mês real:

```bash
python -m src.flows.caged_pipeline 202409
make dbt-build
```

## Camadas

| Camada | Pasta | Conteúdo |
| --- | --- | --- |
| Bronze | `data/bronze/ano=/mes=/tipo=/` | `.7z` + Parquet varchar + metadados |
| Staging/marts | dbt → `data/warehouse/caged.duckdb` | Tipos reais e saldo |
| Gold | `data/gold/` | Exports (reservado) |

Saldo da mart: `sum(saldomovimentação)`, não `count(*)`.
