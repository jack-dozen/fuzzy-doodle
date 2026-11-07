# Log Penggunaan AI

Catat setiap penggunaan AI atau coding agent yang memengaruhi kode atau laporan.

| No | Siapa | Prompt / tugas (ringkas) | Hasil: diterima, diubah, atau ditolak | Alasan | Cara verifikasi |
| --- | --- | --- | --- | --- | --- |
| 1 | Zaky | buatkan test untuk pengecekan operator <> untuk ditambahkan di test_tambahan.py | diterima | Karena konsisten dengan hasil dari crud.cli yang awalnya keliru dengan deteksi not equal menggunakan <>| Membandingkan dengan menjalankan crud.cli, hasilnya terbukti konsisten |
| 2 | Farrel | buatkan test untuk mengeecek kata OUTER yang ada diantara LEFT dan JOIN yang akan saya tambahkan ke test_tambahan.py | diterima | Karena berhasil mendeteksi bug pada sebuah script sql | Membandingkan hasil tes ketika kode yang belum di perbaiki dan sudah diperbaii |
| 3 | Farrel | buatkan test untuk mengeecek presedensi OR dan AND yang akan saya tambahkan ke test_tambahan.py | diterima | Karena berhasil mendeteksi bug pada sebuah script sql | Membandingkan hasil tes ketika kode yang belum di perbaiki dan sudah diperbaii |
| 4 | Zaky | buatkan test alias shadowing untuk di tambah di test_tambahan | diterima | Karena konsisten dengan pengecekan manual | Dibandingkan dengan pengecekan manual dan hasil test yang digenerate AI konsisten |
| 5 | Farrel | Jelaskan mengenai fungsi-fungsi buatan pada resolver.py dan pandu saya dalam mengerjakan TODO(T2) | diterima | Karena kode untuk TODO (T2) membuat hasil test_kolom_tanpa_qualifier_satu_tabel pada test_resolver dari FAIL menjadi PASS | membandingkan hasil test |

**Refleksi.** AI paling membantu kami dalam mencari bug dan membuat test untuk memastikan
perbaikannya. Sejauh penggunaan kami, AI jarang memberikan hasil yang keliru karena spesifikasi
dan konteks codebase yang dibutuhkan tersedia. Kami tetap memeriksa hasil AI, dan pada beberapa
kasus kami yakin karena hasilnya konsisten dengan pengecekan manual atau hasil dari AI lain.
