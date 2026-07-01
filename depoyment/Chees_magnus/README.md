# ♟️ Magnus Chess AI

Sebuah aplikasi antarmuka web interaktif untuk bermain catur melawan model AI kustom yang dilatih menggunakan TensorFlow/Keras. Proyek ini memisahkan logika backend (pengolahan prediksi model AI) dan frontend (UI interaktif menggunakan Streamlit dan Chessboard.js).

## ✨ Fitur Utama
- **Frontend Interaktif:** Menggunakan antarmuka papan catur interaktif (*Drag-and-Drop*) tanpa perlu mengetik teks langkah secara manual.
- **Auto-Move AI:** Ketika Anda selesai melangkah, AI akan merespons secara otomatis tanpa perlu menekan tombol tambahan.
- **Arsitektur Modular:** Memisahkan komponen UI Streamlit dengan mesin pemroses catur di backend.
- **Kustomisasi Model:** Mudah untuk mengganti atau memperbarui bobot model AI Anda di dalam folder `models/`.

## 📂 Struktur Direktori
```text
Chees_magnus/
├── backend/
│   └── chess_engine.py         # Skrip Python pemroses langkah dan prediktor AI
├── frontend/
│   ├── app.py                  # Skrip utama Streamlit
│   └── chessboard_component/   # Komponen kustom Javascript (Chessboard.js)
├── models/
│   └── README.md               # Tempat Anda meletakkan file model_catur_magnus.keras
├── requirements.txt            # Daftar pustaka/dependencies instalasi
└── run_app.bat                 # Script batch pintar untuk menjalankan aplikasi di Windows
```

## 🚀 Cara Menjalankan Aplikasi

### 1. Persiapan Model
Pastikan Anda sudah memiliki model Keras yang telah dilatih (misalnya `model_catur_magnus.keras`).
Pindahkan file model Anda ke dalam direktori `models/`:
```text
Chees_magnus/models/model_catur_magnus.keras
```

### 2. Instalasi Dependensi
Pastikan **Python** (versi 3.8 ke atas disarankan) sudah terinstal di komputer Anda.
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

## ⚙️ Penyesuaian Input Model (Opsional)
Jika arsitektur input data pada model Anda berbeda dari tensor matriks berukuran `(8, 8, 12)`, Anda bisa memodifikasi fungsi `board_to_tensor` dan metode `get_best_move` yang berada pada file `backend/chess_engine.py`.

---
*Dibuat untuk eksperimen AI & Pengembangan Web.*
