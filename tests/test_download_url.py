import pytest

from src.extract.competencia import parse_competencia
from src.extract.download import caged_ftp_url


def test_url_mov_oficial():
    url = caged_ftp_url("202409", "MOV")
    assert url == (
        "ftp://ftp.mtps.gov.br/pdet/microdados/NOVO%20CAGED/"
        "2024/202409/CAGEDMOV202409.7z"
    )


def test_competencia_invalida():
    with pytest.raises(ValueError):
        parse_competencia("202413")
