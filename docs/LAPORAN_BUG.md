# Laporan Bug

## Bug 1: Case Insensitive pada Lexer

**Ditemukan oleh:** Farrel . **Diperbaiki oleh:** Farrel

**Gejala.** Input : "select" dan "from", Output : FAILED, Output yang diharapkan : Nilai token keyword selalu dinormalisasi ke huruf besar.

```sql
select id from t
```

**Akar Permasalahan.** Kode lama salah karena Lexer tidak peka terhadap Token yang seharusnya diidentifikasi sebagai KEYWORD hanya karena huruf kecil dan huruf besar. Konsep yang dilanggar adalah Case Sensitivity / Lexical Grammar (Pengenalan Keyword vs Identifier). Berdasarkan buku Crafting Interpreters, konsep ini dibahas pada Bab 4: Scanning (khususnya mengenai pembedaan antara keyword dan identifier pada Section 4.7 Reserved Words and Identifiers).

**Perbaikan.** Fungsi **_word()** pada file **Lexer** dengan mengubah teks menjadi kapital dengan fungsi **.upper()** dan menyimpan nilainya pada variabel baru (misal upper_text) agar keaslian teks. upper_text inilah yang akan dicek apakah ada di KEYWORD atau tidak. Jika ada, maka masukan upper_text sebagai token KEYWORD. Jika tidak, maka masukan text sebagai token IDENT.

**Test regresi.** test_lexer.py::test_keyword_huruf_kecil.

**Peran AI** tidak ada penggunaan AI pada bug ini.

---

## Bug 2: dua kutip "'" berturut-turut dianggap sebagai kutip penutup

**Ditemukan oleh:** Farrel . **Diperbaiki oleh:** Farrel

**Gejala.** Input : 'O''Brian', Output : FAILED karena menghasilkan dua string yaitu O dan Brian , Output yang diharapkan : PASSED dan menghasilkan satu string O'Brian.

```sql
```

**Akar Permasalahan.** Kode lama salah karena ketika kutip pertama ditemukan dan menemukan kutip berikutnya padahal string belum selesai atau belum habis, lexer menganggap kutip tersebut sebagai penutup string sehingga menghasilkan string O dan string Brian. Konsep yang dilanggar adalah Lexical Grammar / String Literal Scanning. Berdasarkan buku Crafting Interpreters, hal ini terkait dengan aturan scanning string pada Bab 4: Scanning (Section 4.6.1 String literals).

**Perbaikan.** mengecek apakah karakter yang dibaca selanjutnya setelah "'" (kutip seletlah kutip pembuka string) merupakan karakter kutip " ' " lagi dengan menggunakan **match()**. Jika **true**, maka kedua kutip tersebut akan dijadikan satu kutip dan dimasukan kedalam string. Jika **false** maka akan break yang menandai bahwa kutip saat itu adalah kutip penutup string.

**Test regresi.** test_lexer.py::test_dua_kutip_berturut_turut.

**Peran AI** AI membantu saya dalam membuat tes untuk menguji lexernya.

---

## Bug 3: operator not equal (<>) tidak terdeteksi (terdeteksi sebagai operator more than)

**Ditemukan oleh:** Zaky · **Diperbaiki oleh:** Zaky

**Gejala.** Input berupa operator <> dengan harapan outputnya hasil perbandingan not equal bukan more than, sesuai dengan SPESIFIKASI.md bagian 2.5.

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql
WHERE o.status = 'LUNAS' AND o.catatan <> 'FROM rahasia'
```

**Akar masalah.** Dalam kode lama tidak diterapkan pengecekan jika karakter sesudah "<" adalah ">", yang dilakukan hanya pengecekan untuk "<=". Konsep yang dilanggar adalah Two-Character Operators / Lookahead pada Scanner. Berdasarkan buku Crafting Interpreters, scanner memerlukan mekanisme lookahead untuk mengenali operator yang terdiri dari satu atau dua karakter pada Bab 4: Scanning (Section 4.5.2 Operators dan Section 4.6).

**Perbaikan.** Perubahan dilakukan di file lexer.py di dalam fungsi _scan_token karena bagian itu yang bertugas untuk 'memaknai' token, tidak menemukan perbaikan alternatif.

**Test regresi.** test_tambahan::test_operator_tidak_sama_dengan_sudut.

**Peran AI.** Membantu membuat test dalam test_tambahan.py dan memberi tahu file mana yang harus diubah.

---

## Bug 4: subquery dari UPDATE terdeteksi sebagai "U"

**Ditemukan oleh:** AI · **Diperbaiki oleh:** Zaky

**Gejala.** Input berupa script sql yang memiliki query UPDATE dan subquery SET atau WHERE, dalam SPESIFIKASI.md bagian 5 subquery dari UPDATE harus berupa R bukan U, sedangkan dari yang dihasilkan adalah U.

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql
UPDATE pelanggan SET level = 'gold'
WHERE id IN (SELECT pelanggan_id FROM pesanan WHERE total > 1000000);
```

**Akar masalah.** Dalam kode lama subquery menghasilkan U, ini melanggar ketentuan di SPESIFIKASI.md bagian 5. Konsep yang dilanggar adalah Semantic Analysis / Intermediate Representation / AST Node Classification. Berdasarkan buku Crafting Interpreters, hal ini dibahas pada Bab 2: A Map of the Territory (Section 2.1.3 Static analysis dan Section 2.1.4 Intermediate representations) serta Bab 5: Representing Code.

**Perbaikan.** File yang diubah analyzer.py dalam fungsi analyze_statement,

**Test regresi.** test_analyzer::test_matrix_laporan_penjualan.

**Peran AI.** AI secara tidak sengaja menemukan bug ketika saya meminta melakukan hal lainnya (saya minta AI memverifikasi file csv sudah sesuai atau belum untuk mendeteksi bug no 3) kemudian AI memberi tahu kalau dia menemukan bug dimana subquery dari UPDATE ditandai dengan "U" padahal seharusnya ditandai dengan "R".

---

## Bug 5: OUTER ditengah LEFT dan JOIN

**Ditemukan oleh:** AI . **Diperbaiki oleh:** Farrel

**Gejala.** Input : Berupa syntax LEFT JOIN menggunakan OUTER diantara LEFT dan JOIN, Output : FAILED karena parser mengharapkan kata setelah LEFT adalah JOIN padahal ada OUTER , Output yang diharapkan : PASSED karena parser mengecek apakah ada kata OUTER setelah LEFT

```sql
SELECT a.id
FROM a
LEFT OUTER JOIN b
ON b.a_id = a.id
```

**Akar Permasalahan.** Kode lama salah karena pada saat kata LEFT ditemukan oleh **match_kw()**, tidak dilakukan pemeriksaan tambahan apakah ada kata OUTER dan langsung mengharapkan kata selanjutnya adalah JOIN sehingga terjadi parserror. Konsep yang dilanggar adalah Context-Free Grammar / Optional Production Rules. Berdasarkan buku Crafting Interpreters, hal ini dipelajari pada Bab 5: Representing Code (Section 5.1.2 Enhancing our notation) dan Bab 6: Parsing Expressions.

**Perbaikan.** Setelah menemukan kata LEFT, dilakukan pengecekan kata selanjutnya ada OUTER atau tidak dengan menggunakan **match_kw()**. Jika tidak, maka akan mengembalikan none dan tidak akan menggeser pointer. Jika ada, maka akan mengembalikan OUTER dan memindahkan pointer.

**Test regresi.** test_tambahan.py::test_left_join_dengan_outer.

**Peran AI** AI membantu saya dalam membuat tes untuk menguji lexernya.

---

## Bug 5: Presedensi OR dan AND yang setara

**Ditemukan oleh:** AI . **Diperbaiki oleh:** Farrel

**Gejala.** Input : Berupa Script SQL yang berisi penggunaan OR dan AND, Output : FAILED karena parser menganggap AND sebagai ROOT dari ASTnya, Output yang diharapkan : PASSED karena parser membuat OR sebagai ROOT dari ASTnya karena presedensi

```sql
SELECT *
FROM t
WHERE status = 'ACTIVE' OR gaji > 5000 AND umur >= 21;
```

**Akar Permasalahan.** Kode lama salah karena parser mencampur tingkatan OR dan AND pada satu fungsi yaitu **_logical** sehingga hasil dari ASTnya AND sebagai root padahal seharusnya OR sebagai presedensi terendah adalah ROOTnya bukan AND yang berada satu tingkat lebih tinggi dari OR. Ini melanggar konsep Stratified Grammar dan Operator Precedence (Precedence and Associativity) dari buku Crafting Interpreters, di mana setiap level presedensi harus dibuat aturan tata bahasa (grammar) yang terpisah untuk mencegah ambiguitas, yang dibahas pada Bab 6: Parsing Expressions (Section 6.1 Ambiguity and the Parsing Game).

**Perbaikan.** menghapus fungsi **logical()** dan memecahnya menjadi dua fungsi berbeda yaitu **or_expr** dan **and_expr**. fungsi **expr** diubah dari mengembalikan fungsi **logical()** menjadi mengembalikan **or_expr**.

**Test regresi.** test_tambahan.py::test_left_join_dengan_outer.

**Peran AI** AI membantu saya dalam membuat tes untuk menguji parsernya.


## Bug 6: alias shadowing dari dalam ke luar

**Ditemukan oleh:** Farrel · **Diperbaiki oleh:** Zaky

**Gejala.** Misal ada alias yang sama "x" seperti pada sql di bawah ini, seharusnya "x" di luar (merujuk ke pelanggan) di shadow terlebih dahulu oleh "x" di dalam (merujuk ke pesanan), namun malah sebaliknya. Menurut SPESIFIKASI.md scope harusnya di baca yang terdalam.

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql
SELECT x.id
FROM pelanggan x
WHERE x.id IN (SELECT x.pelanggan_id FROM pesanan x WHERE x.total > 500000);
```

**Akar masalah.** Dalam kode lama, dilakukan reverse pada scope, padahal _lookup mengumpulkan scope dari dalam ke luar, sehingga tidak perlu di reverse. Konsep yang dilanggar adalah Lexical Scope and Shadowing. Berdasarkan buku Crafting Interpreters, aturan pencarian nama dari scope terdalam ke scope luar (nesting and shadowing) dibahas secara mendalam pada Bab 8: Statements and State (Section 8.5 Scope, nesting, and shadowing).

**Perbaikan.** File resolver.py di dalam fungsi _lookup(), menghapus reverse(scope) menjadi scope saja.

**Test regresi.** test_tambahan::test_alias_subquery_menutupi_alias_outer.

**Peran AI.** AI membantu membuat test alias shadowing.

---
