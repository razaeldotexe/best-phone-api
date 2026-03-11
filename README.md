# Best Phone Ranking API

API internal berbasis Python Flask untuk mendapatkan peringkat smartphone terbaik berdasarkan agregasi skor dari berbagai sumber benchmark (AnTuTu, Geekbench, DXOMARK, dll).

## Fitur Utama
- **Autentikasi API Key**: Semua request dilindungi header `X-API-Key`.
- **Agregat Skor Berbobot**: Normalisasi skor dari berbagai sumber ke skala 0–100.
- **Cache SQLite**: Data disimpan secara lokal untuk performa tinggi dengan pembaruan otomatis setiap 24 jam.
- **Scraper Engine**: Mendukung scraping dari situs statis dan dinamis (Playwright).

## Struktur Proyek
- `/app`: Logika inti aplikasi (routes, scrapers, database, utils).
- `/tools`: Utilitas tambahan seperti `keygen.py`.
- `run.py`: Entry point untuk menjalankan server.

## Cara Instalasi

1. **Clone repositori**:
   ```bash
   git clone <repository-url>
   cd best-phone-api
   ```

2. **Instal dependensi**:
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

3. **Generate API Key**:
   Jalankan generator untuk membuat kunci baru di file `.env`:
   ```bash
   python tools/keygen.py
   ```

## Cara Penggunaan

### Menjalankan Server
```bash
python run.py
```
Server akan berjalan di `http://127.0.0.1:5000`.

### Endpoint API

| Method | Endpoint | Deskripsi |
| --- | --- | --- |
| `GET` | `/api/v1/phones/ranking` | Daftar smartphone berdasarkan skor. |
| `GET` | `/api/v1/phones/device` | Detail benchmark satu device (`?name=`). |
| `GET` | `/api/v1/cache/status` | Info status dan waktu kedaluwarsa cache. |
| `POST` | `/api/v1/cache/refresh` | Trigger refresh cache secara manual. |

*Pastikan menyertakan header `X-API-Key: <your_key>` pada setiap request.*

## Konfigurasi
Anda dapat mengatur variabel di file `.env`:
- `X_API_KEY`: Kunci keamanan API.
- `DATABASE_URL`: URL database SQLite.
- `CACHE_EXPIRY_HOURS`: Masa berlaku cache (default: 24).
