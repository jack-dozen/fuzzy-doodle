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

## Bug 2: dua kutip "'" berturut-turut dianggap sebagai kutip penutup

**Ditemukan oleh:** Farrel . **Diperbaiki oleh:** Farrel

**Gejala.** Input : 'O''Brian', Output : FAILED karena menghasilkan dua string yaitu O dan Brian , Output yang diharapkan : PASSED dan menghasilkan satu string O'Brian.

```sql
```

**Akar Permasalahan.** Kode lama salah karena ketika kutip pertama ditemukan dan menemukan kutip berikutnya padahal string belum selesai atau belum habis, lexer menganggap kutip tersebut sebagai penutup string sehingga menghasilkan string O dan string Brian.

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

**Akar masalah.** Dalam kode lama tidak diterapkan pengecekan jika karakter sesudah "<" adalah ">", yang dilakukan hanya pengecekan untuk "<=".

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

**Akar masalah.** Dalam kode lama subquery menghasilkan U, ini melanggar ketentuan di SPESIFIKASI.md bagian 5.

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

**Akar Permasalahan.** Kode lama salah karena pada saat kata LEFT ditemukan oleh **match_kw()**, tidak dilakukan pemeriksaan tambahan apakah ada kata OUTER dan langsung mengharapkan kata selanjutnya adalah JOIN sehingga terjadi parserror.

**Perbaikan.** Setelah menemukan kata LEFT, dilakukan pengecekan kata selanjutnya ada OUTER atau tidak dengan menggunakan **match_kw()**. Jika tidak, maka akan mengembalikan none dan tidak akan menggeser pointer. Jika ada, maka akan mengembalikan OUTER dan memindahkan pointer.

**Test regresi.** test_tambahan.py::test_left_join_dengan_outer.

**Peran AI** AI membantu saya dalam membuat tes untuk menguji lexernya.
