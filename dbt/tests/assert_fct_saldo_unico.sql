select competencia, uf, secao
from {{ ref("fct_saldo_mensal") }}
group by competencia, uf, secao
having count(*) > 1
