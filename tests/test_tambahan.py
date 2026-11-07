import pytest

from crud.lexer import LexError, TokenType as T, tokenize
from crud import ast_nodes as ast
from crud.parser import parse_sql
from crud.ast_nodes import pretty
from crud.resolver import Resolver
from crud.analyzer import analyze_statement, column_usage

"""Test tambahan buatan kelompok.

Isi dengan:
1. Satu test regresi untuk setiap bug yang kalian perbaiki (gagal sebelum perbaikan,
   lulus sesudahnya). Beri nama yang menjelaskan bug-nya.
2. Lima test kasus tepi, masing-masing dengan komentar singkat mengapa kasus itu berisiko.
"""

#Lexer
def test_kombinasi_huruf_besar_dan_huruf_kecil():
    toks = tokenize("SelEct id fRom t")
    assert toks[0].type == T.KEYWORD and toks[0].value == "SELECT"
    assert toks[2].type == T.KEYWORD and toks[2].value == "FROM"
#ini penting untuk membangun lexer yang case sensitive

#Edge case Lexer
def test_dua_kutip_berturut_turut():
    toks = tokenize("'O''Brian'")
    assert toks[0].type == T.STRING and toks[0].value == "O'Brian"
#Jika Lexer salah menganggap kutip kedua sebagai penutup string, 
#pembacaan token setelahnya akan acak-acakan dan merusak seluruh parsing file SQL tersebut.

#Edge case lexer 2
def test_lexer_unclosed_block_comment():
    with pytest.raises(LexError) as exc_info:
        tokenize("SELECT /* komentar gantung")
    assert "Komentar tidak di tutup" in str(exc_info.value)
#Komentar blok /*.. */ dapat melewati banyak baris. Jika input SQL terpotong di pertengahan komentar (tidak ditutup hingga EOF),
#maka Lexer harus mampu menghentikan proses dan melempar LexError agar tidak terjebak di infinite loop atau meloloskan input SQL yang tidak valid


def test_operator_tidak_sama_dengan_sudut():
    toks = tokenize("a <> b")
    assert [(tok.type, tok.value) for tok in toks] == [
        (T.IDENT, "a"),
        (T.OP, "<>"),
        (T.IDENT, "b"),
        (T.EOF, ""),
    ]

#Parser
def one(sql):
    script = parse_sql(sql)
    assert script.errors == [], script.errors
    assert len(script.statements) == 1
    return script.statements[0]

def test_left_join_dengan_outer():
    s = one("SELECT a.id FROM a LEFT OUTER JOIN b ON b.a_id = a.id")
    assert s.joins[0].kind == "LEFT"
    assert s.joins[0].source.name == "b"

def test_presedensi_and_or():
    sql = "SELECT * FROM t WHERE status = 'ACTIVE' OR gaji > 5000 AND umur >= 21;"
    script = parse_sql(sql)

    #Menampilkan AST
    print(pretty(script.statements[0].where))

    # 1. Pastikan tidak ada error parsing
    assert len(script.errors) == 0

    # 2. Ambil node ekspresi WHERE
    where_expr = script.statements[0].where

    # 3. Uji hierarki AST
    assert isinstance(where_expr, ast.BinaryOp)
    assert where_expr.op == "OR"          # Root harus OR
    assert where_expr.left.op == "="      # Sisi kiri OR adalah status = 'ACTIVE'
    assert where_expr.right.op == "AND"   # Sisi kanan OR diikat oleh AND

#Edge Case 3
def test_parser_between_with_logical_and():
    script = parse_sql("SELECT * FROM t WHERE x BETWEEN 10 AND 20 AND y = 5;")
    stmt = script.statements[0]
    # Root WHERE haruslah AND logika
    assert isinstance(stmt.where, ast.BinaryOp)
    assert stmt.where.op == "AND"
    assert isinstance(stmt.where.left, ast.Between)
#Kata kunci AND memiliki peran ganda di SQL: sebagai pembatas BETWEEN ... AND ... sekaligus sebagai operator logika perbandingan. 
# Parser dengan presedensi bertingkat (stratified grammar) yang benar harus memastikan AND pertama diserap oleh Between, sedangkan AND kedua menjadi root BinaryOp utama. 
# Jika parsing ambigu, struktur hirarki AST akan salah.

def test_synchronize_panic_mode():
    sql = """
    SELECT a FORM b;
    SELECT buah FROM produk
    """

    script = parse_sql(sql)

    assert len(script.errors) == 1

    assert len(script.statements) == 1
    assert script.statements[0].sources[0].name == "produk"

#Test Regresi dan Edge case 4 resolver
def test_alias_subquery_menutupi_alias_outer():
    sql = "SELECT p.id FROM pelanggan p WHERE p.id IN (SELECT p.id FROM pesanan p)"
    script = parse_sql(sql)
    assert script.errors == [], script.errors

    diagnostics = Resolver().resolve_script(script)
    column_refs = [
        node for node in ast.iter_nodes(script)
        if isinstance(node, ast.ColumnRef)
    ]

    assert [column.resolved for column in column_refs] == [
        "pelanggan",
        "pelanggan",
        "pesanan",
    ]
    assert diagnostics == []

#Edge Case 5 (Analyzer)
def test_analyzer_self_referencing_insert():
    script = parse_sql("INSERT INTO crm.pelanggan SELECT * FROM crm.pelanggan;")
    stmt = script.statements[0]

    matrix = analyze_statement(stmt)

    assert matrix["crm.pelanggan"] == {"C", "R"}

