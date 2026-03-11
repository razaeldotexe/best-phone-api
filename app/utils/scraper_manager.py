import threading
import time
import random
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

    def run_refresh(self):
        with self.app.app_context():
            print(f"[{datetime.now()}] Starting full cache refresh for latest flagships...")
            
            # 1. Dapatkan daftar flagship terbaru dari GSMArena
            flagships = self.scrapers["gsmarena"].get_latest_flagships(limit=10)
            print(f"Found {len(flagships)} flagship candidates: {flagships}")

            for target_device in flagships:
                print(f"Processing {target_device}...")
                
                # Gunakan GSMArenaScraper untuk mendapatkan data riil
                real_data = self.scrapers["gsmarena"].scrape_device(target_device)
                
                if not real_data:
                    print(f"Failed to fetch real data for {target_device}")
                    continue

                # Hitung skor agregat berdasarkan data yang ditemukan
                # Untuk demo, kita gunakan skor dasar dari GSMArena dan mock sisanya jika tidak ada
                antutu_raw = real_data["scores"].get("antutu", 1500000)
                geek_raw = real_data["scores"].get("geekbench", 6000)
                
                # Normalisasi sederhana (asumsi max Antutu 2.5jt, Geekbench 10rb)
                scores_for_agg = {
                    "antutu": (antutu_raw / 2500000) * 100,
                    "geekbench": (geek_raw / 10000) * 100,
                    "dxomark": 80 + (antutu_raw / 100000), # Mock logic berdasarkan performa
                    "d3dmark": 80 + (geek_raw / 500),
                    "nanoreview": 90,
                    "kimovil": 9.2
                }
                
                real_data["aggregate_score"] = calculate_aggregate_score(scores_for_agg)
                
                # Simpan ke database (berdasarkan nama unik yang diekstrak)
                device = DeviceCache.query.filter_by(name=real_data["name"]).first()
                if not device:
                    device = DeviceCache(name=real_data["name"])
                    db.session.add(device)
                
                device.data = real_data
                device.updated_at = datetime.utcnow()
                
                # Commit bertahap agar data tidak hilang jika terputus
                db.session.commit()
                print(f"Successfully cached {real_data['name']}")
                
                # Jeda antar perangkat agar tidak membombardir server (tambahan 5-10 detik)
                time.sleep(random.uniform(5.0, 10.0))

            # Update metadata akhir
            metadata = CacheMetadata.query.first()
            if not metadata:
                metadata = CacheMetadata()
                db.session.add(metadata)
            
            metadata.last_update = datetime.utcnow()
            metadata.device_count = DeviceCache.query.count()
            db.session.commit()
            
            print(f"[{datetime.now()}] Full cache refresh completed. Total devices: {metadata.device_count}")

    def schedule_auto_refresh(self):
        def refresh_loop():
            while True:
                self.run_refresh()
                time.sleep(24 * 3600)  # 24 hours
        
        thread = threading.Thread(target=refresh_loop, daemon=True)
        thread.start()
