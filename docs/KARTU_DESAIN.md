# Kartu Desain

Tuliskan lima keputusan desain penting dalam pekerjaan kalian. Untuk tiap keputusan, sebutkan
alternatif yang ditolak dan alasannya. Contoh topik (boleh memilih yang lain):

- bagaimana parser membedakan `*` sebagai "semua kolom" dan sebagai perkalian;
- di mana dan bagaimana presedensi `AND`/`OR` dinyatakan;
- mengapa error recovery berhenti di `;`, bukan di keyword `SELECT` berikutnya;
- urutan pencarian scope dan akibatnya pada shadowing serta correlated subquery;
- mengapa kolom tanpa qualifier hanya dilihat di scope terdalam, dan apa kelemahannya;
- bagaimana implementasi `INSERT ... SELECT` atau komentar blok kalian.

| No | Keputusan | Alternatif yang ditolak | Alasan |
| --- | --- | --- | --- |
| 1 | error recovery berhenti safe-point seperti ketika ketemu semicolon (;) atau keyword pembuka statement (select,insert,update,delete) | safe-point hanya semicolon saja atau keyword pembuka statement saja | Hal ini karena sesuai dengan konsep panic mode recovery error pada crafting interpreters dimana semicolon dan keyword pembuka dijadikan safe-point sebagai penanda statement baru |
| 2 | OR dan AND dibuatkan fungsi masing-masing dimana OR sebagai tingkat terendah akan menjadi root dan akan memanggil AND yang satu tingkat diatasnya, sedangkan AND akan memanggil NOT | - | Hal ini dilakukan karena AND bisa saja menjadi ROOT akibat kode membuat OR dan AND berada pada tingkat yang sama padahal OR sebagai tingkat terendah haruslah menjadi ROOT |
| 3 | | | |
| 4 | | | |
| 5 | | | |
