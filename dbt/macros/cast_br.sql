{% macro br_int(expr) %}
try_cast({{ expr }} as integer)
{% endmacro %}

{% macro br_num(expr) %}
try_cast(replace(cast({{ expr }} as varchar), ',', '.') as double)
{% endmacro %}
