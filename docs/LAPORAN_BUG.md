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