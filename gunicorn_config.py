import multiprocessing

# Alamat dan port untuk bind
bind = "0.0.0.0:5000"

# Jumlah worker: (2 x cores) + 1
workers = multiprocessing.cpu_count() * 2 + 1

# Nama proses
proc_name = "best_phone_api"

# Logging
accesslog = "access.log"
errorlog = "error.log"
loglevel = "info"

# Timeout: Berikan waktu lebih untuk scraper (scraper manager berjalan di thread lain)
timeout = 120

# Daemon mode tidak digunakan di systemd service
daemon = False
