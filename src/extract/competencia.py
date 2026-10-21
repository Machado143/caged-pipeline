"""Validação de competência AAAAMM."""

from __future__ import annotations

import re

_COMPETENCIA = re.compile(r"^(20\d{2})(0[1-9]|1[0-2])$")


def parse_competencia(competencia: str) -> tuple[str, str]:
    """Retorna (ano, mes) com dois dígitos."""
    valor = str(competencia).strip()
    match = _COMPETENCIA.match(valor)
    if not match:
        raise ValueError(f"Competência inválida (use AAAAMM): {competencia!r}")
    return match.group(1), match.group(2)
