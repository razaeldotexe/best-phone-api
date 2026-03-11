import urllib.parse
import re
from .base import BaseScraper

class GSMArenaScraper(BaseScraper):
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.gsmarena.com"

    def search_device(self, device_name):
        """Mencari perangkat di GSMArena dan mengembalikan URL halaman spesifikasinya."""
        query = urllib.parse.quote(device_name)
        search_url = f"{self.base_url}/results.php3?sQuickSearch=yes&sName={query}"
        
        try:
            soup = self.fetch_page(search_url)
            # GSMArena biasanya menampilkan hasil pencarian dalam div class 'makers'
            makers_div = soup.find('div', class_='makers')
            if not makers_div:
                return None
            
            first_device = makers_div.find('a')
            if not first_device:
                return None
            
            return f"{self.base_url}/{first_device['href']}"
        except Exception as e:
            print(f"Error searching GSMArena for {device_name}: {e}")
            return None

    def scrape_device(self, device_name):
        """Mengekstrak data riil dari halaman spesifikasi GSMArena."""
        device_url = self.search_device(device_name)
        if not device_url:
            return None

        try:
            soup = self.fetch_page(device_url)
            
            data = {
                "name": soup.find('h1', class_='specs-phone-name-title').text.strip(),
                "brand": device_name.split()[0], # Asumsi brand adalah kata pertama
                "scores": {},
                "price_usd": "N/A",
                "sources": {
                    "gsmarena": device_url
                },
                "thumbnail_url": soup.find('div', class_='specs-photo-main').find('img')['src'] if soup.find('div', class_='specs-photo-main') else None
            }

            # Ekstrak Harga
            price_row = soup.find('td', class_='ttl', string=re.compile('Price', re.I))
            if price_row:
                price_info = price_row.find_next_sibling('td', class_='nfo')
                if price_info:
                    # GSMArena sering menampilkan harga dalam format: $ 1,000 / £ 800 ...
                    price_text = price_info.text.strip()
                    match = re.search(r'\$\s*([\d,.]+)', price_text)
                    if match:
                        data["price_usd"] = match.group(1)

            # Ekstrak Benchmark (Performance)
            perf_row = soup.find('td', class_='ttl', string=re.compile('Performance', re.I))
            if perf_row:
                perf_info = perf_row.find_next_sibling('td', class_='nfo')
                if perf_info:
                    perf_text = perf_info.text.strip()
                    # Contoh text: AnTuTu: 1823822 (v10), GeekBench: 7076 (v6), GFXBench: 121fps (ES 3.1 onscreen)
                    
                    # AnTuTu
                    antutu_match = re.search(r'AnTuTu:\s*([\d,]+)', perf_text)
                    if antutu_match:
                        data["scores"]["antutu"] = int(antutu_match.group(1).replace(',', ''))
                    
                    # Geekbench
                    geek_match = re.search(r'GeekBench:\s*([\d,]+)', perf_text)
                    if geek_match:
                        data["scores"]["geekbench"] = int(geek_match.group(1).replace(',', ''))

            return data
        except Exception as e:
            print(f"Error scraping GSMArena device {device_name}: {e}")
            return None
