# Laporan Bug

Salin blok di bawah untuk setiap bug. Bagian **Akar masalah** wajib ditulis dengan kata-kata
sendiri dan memakai konsep dari *Crafting Interpreters* (sebutkan bab). Bagian ini diuji lisan.

---

## Bug 1: (judul singkat)

**Ditemukan oleh:** (nama) · **Diperbaiki oleh:** (nama)

**Gejala.** Input, output yang didapat, dan output yang diharapkan menurut SPESIFIKASI.md
(sebutkan bagiannya).

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql

```

**Akar masalah.** Mengapa kode lama salah? Konsep apa yang dilanggar?

**Perbaikan.** File dan fungsi yang diubah, serta alasannya. Sebutkan juga perbaikan
alternatif yang kalian pertimbangkan dan alasan tidak memilihnya.

**Test regresi.** Nama test di `tests/test_tambahan.py` yang gagal sebelum perbaikan dan lulus
sesudahnya.

**Peran AI.** Apakah AI membantu menemukan atau memperbaiki bug ini? Bagaimana kalian
memverifikasinya?

---

## Bug 1: Case Insensitive pada Lexer

**Ditemukan oleh:** Farrel . **Diperbaiki oleh:** Farrel

**Gejala.** Input : "select" dan "from", Output : FAILED, Output yang diharapkan : Nilai token keyword selalu dinormalisasi ke huruf besar. 

```sql
select id from t
```

**Akar Permasalahan.** Kode lama salah karena Lexer tidak peka terhadap Token yang seharusnya diidentifikasi sebagai KEYWORD hanya karena huruf kecil dan huruf besar. Konsep yang dilanggar adalah Case sensitivity.

**Perbaikan.** Fungsi **_word()** pada file **Lexer** dengan mengubah teks menjadi kapital dengan fungsi **.upper()** dan menyimpan nilainya pada variabel baru (misal upper_text) agar keaslian teks. upper_text inilah yang akan dicek apakah ada di KEYWORD atau tidak. Jika ada, maka masukan upper_text sebagai token KEYWORD. Jika tidak, maka masukan text sebagai token IDENT.

**Test regresi.** test_lexer.py::test_keyword_huruf_kecil.

**Peran AI** tidak ada penggunaan AI pada bug ini.

---