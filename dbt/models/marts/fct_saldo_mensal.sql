{{ config(materialized="table") }}

select
    competenciamov as competencia,
    uf,
    secao,
    sum(saldomovimentacao) as saldo,
    sum(case when saldomovimentacao = 1 then 1 else 0 end) as admissoes,
    sum(case when saldomovimentacao = -1 then 1 else 0 end) as desligamentos,
    count(*) as qtd_movimentacoes
from {{ ref("int_caged_movimentacoes") }}
group by competenciamov, uf, secao
