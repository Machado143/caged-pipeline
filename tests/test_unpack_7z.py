from pathlib import Path

import py7zr

from src.extract.unpack import unpack_archive


def test_unpack_7z(tmp_path: Path):
    txt = tmp_path / "CAGEDMOV202301.txt"
    txt.write_text("competênciamov\n202301\n", encoding="utf-8")
    archive = tmp_path / "CAGEDMOV202301.7z"
    with py7zr.SevenZipFile(archive, mode="w") as zf:
        zf.write(txt, txt.name)

    destino = tmp_path / "out"
    arquivos = unpack_archive(archive, destino)
    extraido = destino / "CAGEDMOV202301.txt"
    assert extraido in arquivos
    assert extraido.read_text(encoding="utf-8").startswith("competênciamov")
