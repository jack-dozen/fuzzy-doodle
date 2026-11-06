# Log Penggunaan AI

Catat setiap penggunaan AI atau coding agent yang memengaruhi kode atau laporan.

| No | Siapa | Prompt / tugas (ringkas) | Hasil: diterima, diubah, atau ditolak | Alasan | Cara verifikasi |
| --- | --- | --- | --- | --- | --- |
| 1 | Zaky | buatkan test untuk pengecekan operator <> untuk ditambahkan di test_tambahan.py | diterima | Karena konsisten dengan hasil dari crud.cli yang awalnya keliru dengan deteksi not equal menggunakan <>| Membandingkan dengan menjalankan crud.cli, hasilnya terbukti konsisten |
| 2 | Farrel | buatkan test untuk mengeecek kata OUTER yang ada diantara LEFT dan JOIN yang akan saya tambahkan ke test_tambahan.py | diterima | Karena berhasil mendeteksi bug pada sebuah script sql | Membandingkan hasil tes ketika kode yang belum di perbaiki dan sudah diperbaii |
| 3 | Farrel | buatkan test untuk mengeecek presedensi OR dan AND yang akan saya tambahkan ke test_tambahan.py | diterima | Karena berhasil mendeteksi bug pada sebuah script sql | Membandingkan hasil tes ketika kode yang belum di perbaiki dan sudah diperbaii |

**Refleksi (3-5 kalimat).** Di bagian mana AI paling membantu? Di mana AI keliru atau
menyesatkan, dan bagaimana kalian mengetahuinya?
