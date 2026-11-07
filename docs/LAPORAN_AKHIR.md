# Laporan Akhir

## 1. Hasil evaluasi

Hasil menjalankan `python evaluate.py`:

```text
Dievaluasi: audit.sql, campuran_error.sql, laporan_penjualan.sql, pemeliharaan.sql (27 triple)

Metode   Precision  Recall     F1
parser        1.00    1.00   1.00
regex         0.65    0.81   0.72

[regex]
  salah ditemukan (FP): ('audit.sql', 16, 'sesi', 'R')
  salah ditemukan (FP): ('campuran_error.sql', 4, 'pesanan', 'R')
  salah ditemukan (FP): ('campuran_error.sql', 8, 'keranjang', 'R')
  salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'pelanggan', 'D')
  salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'pelanggan', 'R')
  salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'pesanan', 'R')
  salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'rahasia', 'R')
  salah ditemukan (FP): ('laporan_penjualan.sql', 15, 'pesanan', 'R')
  salah ditemukan (FP): ('pemeliharaan.sql', 2, 'crm.alamat', 'R')
  salah ditemukan (FP): ('pemeliharaan.sql', 2, 'crm.pelanggan', 'R')
  salah ditemukan (FP): ('pemeliharaan.sql', 2, 'pelanggan_lama', 'U')
  salah ditemukan (FP): ('pemeliharaan.sql', 15, 'crm.alamat', 'R')
  terlewat (FN):       ('audit.sql', 2, 'pesanan', 'R')
  terlewat (FN):       ('laporan_penjualan.sql', 3, 'pelanggan', 'R')
  terlewat (FN):       ('laporan_penjualan.sql', 3, 'pesanan', 'R')
  terlewat (FN):       ('pemeliharaan.sql', 3, 'crm.alamat', 'R')
  terlewat (FN):       ('pemeliharaan.sql', 3, 'crm.pelanggan', 'R')
```

## 2. Tiga kasus di mana regex salah

1. Pada `audit.sql` baris 16, terdapat `DELETE FROM sesi s WHERE s.kedaluwarsa < :sekarang;`. Regex menghasilkan operasi R untuk `sesi` karena menemukan pola `FROM sesi`, padahal pola `DELETE FROM` menghasilkan operasi D. Parser benar karena memahami bahwa `FROM` pada statement tersebut merupakan bagian dari `DELETE`, sehingga operasi untuk `sesi` adalah D, bukan R.
2. Pada `laporan_penjualan.sql` baris 2, terdapat komentar `-- DELETE FROM pelanggan   (baris ini komentar, bukan perintah)`. Regex tetap menemukan pola `DELETE FROM pelanggan` dan menghasilkan operasi D, padahal teks tersebut adalah komentar. Parser benar karena lexer mengabaikan komentar, sehingga komentar tidak masuk ke hasil CRUD.
3. Pada `audit.sql` baris 2, query pertama menggunakan `FROM pelanggan p, pesanan o`. Regex menemukan `pelanggan`, tetapi melewatkan `pesanan` karena nama tabel kedua tidak didahului keyword `FROM` atau `JOIN`. Parser benar karena mem-parsing kedua tabel yang dipisahkan koma sebagai sumber query, sehingga keduanya dicatat sebagai R.

## 3. Batas pendekatan kami

1. **Komentar yang berisi SQL.** Contohnya `-- DELETE FROM pelanggan` di `laporan_penjualan.sql`. Regex dapat menghasilkan D untuk `pelanggan` meskipun perintah itu hanya komentar. Akibatnya, CRUD matrix memuat operasi yang sebenarnya tidak dijalankan. Untuk membedakannya, extractor perlu mengetahui apakah teks berada di dalam komentar, termasuk komentar satu baris dan komentar blok.
2. **String yang berisi kata kunci SQL.** Contohnya kondisi `o.catatan <> 'FROM rahasia'` di `laporan_penjualan.sql`. Regex dapat mengira `rahasia` adalah tabel yang dibaca dan menambahkan operasi R. Akibatnya, CRUD matrix memiliki tabel dan operasi palsu. Untuk mengatasinya, extractor perlu mengetahui batas string serta escape kutip agar kata `FROM` di dalam string tidak dianggap sebagai keyword.
3. **Bentuk daftar tabel yang tidak selalu diawali `FROM` atau `JOIN`.** Contohnya `FROM pelanggan p, pesanan o` di `audit.sql`. Regex hanya menemukan tabel setelah `FROM`, sehingga operasi R untuk `pesanan` terlewat. Akibatnya, CRUD matrix tidak mencatat semua tabel sumber. Untuk mengatasinya, extractor perlu mengetahui aturan sintaks `FROM` dan mem-parsing setiap table reference, termasuk yang dipisahkan koma.

## 4. Pembagian kerja

Kami tidak membagi pekerjaan secara khusus dari awal. Siapa yang menemukan bug akan mencoba memperbaikinya, jika belum bisa memperbaiki bug tersebut, pekerjaan akan diberikan kepada anggota yang lain. Untuk memastikan kami memahami kode, masing-masing menjelaskan bagian yang diperbaiki kepada anggota lainnya dan melakukan tracing manual bersama.
