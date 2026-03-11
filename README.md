# Best Phone Ranking API

API internal berbasis Python Flask untuk mendapatkan peringkat smartphone terbaik berdasarkan agregasi skor dari berbagai sumber benchmark (AnTuTu, Geekbench, DXOMARK, dll).

## Fitur Utama
- **Publik API**: Semua endpoint dapat diakses secara langsung tanpa autentikasi.
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

*Semua endpoint sekarang dapat diakses secara bebas tanpa header tambahan.*

## Konfigurasi
Anda dapat mengatur variabel di file `.env`:
- `X_API_KEY`: Kunci keamanan API (Opsional).
- `DATABASE_URL`: URL database SQLite.
- `CACHE_EXPIRY_HOURS`: Masa berlaku cache (default: 24).

---

## Deployment ke VPS Linux (Ubuntu)

1. **Persiapan Sistem**:
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv nginx
   ```

2. **Setup Direktori & Virtual Environment**:
   ```bash
   sudo mkdir -p /var/www/best-phone-api
   sudo chown $USER:$USER /var/www/best-phone-api
   # Upload code ke folder tersebut
   cd /var/www/best-phone-api
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   playwright install chromium
   # Instal dependensi sistem untuk playwright
   sudo playwright install-deps
   ```

3. **Konfigurasi Systemd Service**:
   ```bash
   sudo cp best_phone_api.service /etc/systemd/system/
   sudo systemctl start best_phone_api
   sudo systemctl enable best_phone_api
   ```

4. **Konfigurasi Nginx**:
   ```bash
   sudo cp nginx_config.conf /etc/nginx/sites-available/best_phone_api
   sudo ln -s /etc/nginx/sites-available/best_phone_api /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```
