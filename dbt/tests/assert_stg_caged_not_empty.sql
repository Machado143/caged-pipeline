select 1
from {{ ref("stg_caged") }}
having count(*) = 0
