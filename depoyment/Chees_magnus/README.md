# ♟️ Magnus Chess AI Arena

Sebuah aplikasi antarmuka web interaktif modern untuk bermain catur melawan AI. Proyek ini memisahkan logika backend (engine catur) dan frontend (UI interaktif Streamlit + Chessboard.js).

## ✨ Fitur Utama
- **UI/UX Modern:** Tampilan gaya dashboard, panel status game, histori langkah, dan desain responsif untuk desktop/mobile.
- **Frontend Interaktif:** Papan catur drag-and-drop tanpa input teks langkah.
- **Auto-Move AI:** AI bergerak otomatis saat giliran hitam.
- **Fallback Engine Cerdas:** Jika model TensorFlow tidak tersedia, engine tetap berjalan dengan heuristik material (lebih baik dari random).
- **Arsitektur Modular:** Pemisahan komponen UI dan mesin catur backend.

## 📂 Struktur Direktori
```text
Chees_magnus/
├── backend/
│   └── chess_engine.py         # Skrip Python pemroses langkah dan prediktor AI
├── frontend/
│   ├── app.py                  # Skrip utama Streamlit
│   └── chessboard_component/   # Komponen kustom Javascript (Chessboard.js)
├── requirements.txt            # Daftar pustaka/dependencies instalasi
└── run_app.bat                 # Script batch pintar untuk menjalankan aplikasi di Windows
```

## 🚀 Cara Menjalankan Aplikasi

### 1. (Opsional) Persiapan Model TensorFlow
Anda bisa menaruh model `model_catur_magnus.keras` di salah satu lokasi berikut:

- `Chees_magnus/models/model_catur_magnus.keras`
- root proyek: `model_catur_magnus.keras`

Jika model tidak ada, aplikasi tetap berjalan menggunakan fallback engine heuristik.

### 2. Instalasi Dependensi
Pastikan **Python** (versi 3.10+ disarankan) sudah terinstal di komputer Anda.
Buka Terminal/Command Prompt di dalam folder proyek ini, dan jalankan perintah berikut untuk menginstal pustaka yang diperlukan:
```bash
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi
Di komputer Windows, Anda cukup melakukan **klik-ganda (double-click)** pada file `run_app.bat`.
Aplikasi secara otomatis akan membuka halaman web di *browser* default Anda (berjalan di localhost, biasanya pada `http://localhost:8501`).

Jika Anda menggunakan OS lain atau ingin menjalankannya lewat terminal:
```bash
python -m streamlit run frontend/app.py
```

## ☁️ Deploy ke Streamlit Community Cloud

1. Push proyek Anda ke GitHub.
2. Buka Streamlit Community Cloud, lalu klik **Create app**.
3. Pilih repository: `YoungTheBeginner/chess-magnus`.
4. Isi **Main file path** dengan:
	```text
	depoyment/Chees_magnus/frontend/app.py
	```
5. Deploy.

Catatan:
- Agar deploy ringan dan stabil, `requirements.txt` hanya memuat dependency runtime utama.
- Jika ingin memakai model TensorFlow di cloud, tambahkan paket TensorFlow secara manual lalu pastikan resource server mencukupi.

## ⚙️ Penyesuaian Engine
Jika arsitektur input data model Anda berbeda dari tensor `(8, 8, 12)`, ubah fungsi `board_to_tensor` dan strategi pemilihan langkah pada `backend/chess_engine.py`.

---
*Dibuat untuk eksperimen AI & Pengembangan Web.*
