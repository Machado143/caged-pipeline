{{ config(materialized="view") }}

select *
from {{ ref("stg_caged") }}
where
    _tipo_arquivo = 'MOV'
    and saldomovimentacao in (1, -1)
