import pytest

from crud.lexer import LexError, TokenType as T, tokenize

"""Test tambahan buatan kelompok.

Isi dengan:
1. Satu test regresi untuk setiap bug yang kalian perbaiki (gagal sebelum perbaikan,
   lulus sesudahnya). Beri nama yang menjelaskan bug-nya.
2. Lima test kasus tepi, masing-masing dengan komentar singkat mengapa kasus itu berisiko.
"""

def test_kombinasi_huruf_besar_dan_huruf_kecil():
    toks = tokenize("SelEct id fRom t")
    assert toks[0].type == T.KEYWORD and toks[0].value == "SELECT"
    assert toks[2].type == T.KEYWORD and toks[2].value == "FROM"
#ini penting untuk membangun lexer yang case sensitive

def test_dua_kutip_berturut_turut():
    toks = tokenize("'O''Brian'")
    assert toks[0].type == T.STRING and toks[0].value == "O'Brian"