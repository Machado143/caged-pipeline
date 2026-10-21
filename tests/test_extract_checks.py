from pathlib import Path

import pytest

from src.extract.checks import check_extracted_files


def test_check_extracted_files_ok(tmp_path: Path):
    f = tmp_path / "a.csv"
    f.write_text("x")
    assert check_extracted_files(tmp_path) == [f]


def test_check_extracted_files_vazio(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        check_extracted_files(tmp_path)
