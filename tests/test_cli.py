import csv

from crud.cli import main


def test_cli_combines_wildcard_files_into_one_matrix(tmp_path):
    (tmp_path / "a.sql").write_text("INSERT INTO pelanggan (id) VALUES (1)", encoding="utf-8")
    (tmp_path / "b.sql").write_text("DELETE FROM pesanan WHERE id = 1", encoding="utf-8")
    output = tmp_path / "matrix.csv"

    assert main([str(tmp_path / "*.sql"), "--out", str(output)]) == 0

    with output.open(encoding="utf-8", newline="") as file:
        rows = list(csv.reader(file))

    assert rows == [
        ["file", "pelanggan", "pesanan"],
        ["a.sql", "C", ""],
        ["b.sql", "", "D"],
    ]
