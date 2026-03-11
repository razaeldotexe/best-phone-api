import threading
import time
from datetime import datetime
from app.database import db, DeviceCache, CacheMetadata
from app.scrapers import GSMArenaScraper, AntutuScraper
from app.utils.scoring import calculate_aggregate_score
import json

class ScraperManager:
    def __init__(self, app):
        self.app = app
        self.scrapers = {
            "gsmarena": GSMArenaScraper(),
            "antutu": AntutuScraper(),
            # Add others here
        }

    def run_refresh(self, target_device="Samsung Galaxy S24 Ultra"):
        with self.app.app_context():
            print(f"[{datetime.now()}] Starting cache refresh for {target_device}...")
            
            # Gunakan GSMArenaScraper untuk mendapatkan data riil
            real_data = self.scrapers["gsmarena"].scrape_device(target_device)
            
            if not real_data:
                print(f"Failed to fetch real data for {target_device}")
                return

            # Hitung skor agregat berdasarkan data yang ditemukan
            # Untuk demo, kita gunakan skor dasar dari GSMArena dan mock sisanya jika tidak ada
            antutu_raw = real_data["scores"].get("antutu", 1800000)
            geek_raw = real_data["scores"].get("geekbench", 7000)
            
            # Normalisasi sederhana untuk demo (asumsi max Antutu 2.5jt, Geekbench 10rb)
            scores_for_agg = {
                "antutu": (antutu_raw / 2500000) * 100,
                "geekbench": (geek_raw / 10000) * 100,
                "dxomark": 85, # Mock sisanya sementara
                "d3dmark": 88,
                "nanoreview": 92,
                "kimovil": 9.4
            }
            
            real_data["aggregate_score"] = calculate_aggregate_score(scores_for_agg)
            
            device = DeviceCache.query.filter_by(name=real_data["name"]).first()
            if not device:
                device = DeviceCache(name=real_data["name"])
                db.session.add(device)
            
            device.data = real_data
            device.updated_at = datetime.utcnow()
            
            # Update metadata
            metadata = CacheMetadata.query.first()
            if not metadata:
                metadata = CacheMetadata()
                db.session.add(metadata)
            
            metadata.last_update = datetime.utcnow()
            metadata.device_count = DeviceCache.query.count()
            
            db.session.commit()
            print(f"[{datetime.now()}] Cache refresh completed.")

    def schedule_auto_refresh(self):
        def refresh_loop():
            while True:
                self.run_refresh()
                time.sleep(24 * 3600)  # 24 hours
        
        thread = threading.Thread(target=refresh_loop, daemon=True)
        thread.start()
