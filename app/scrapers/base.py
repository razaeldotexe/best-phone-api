import random
import time
import httpx
from bs4 import BeautifulSoup

class BaseScraper:
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1"
        ]
        self.client = httpx.Client(timeout=30.0, follow_redirects=True)

    def get_headers(self):
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/",
            "DNT": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
        }

    def fetch_page(self, url, retries=3, initial_delay=5.0):
        for i in range(retries):
            try:
                # Tambahkan delay acak dasar
                wait_time = initial_delay * (2 ** i) + random.uniform(1, 5)
                if i > 0:
                    print(f"Retry {i}/{retries} for {url} after waiting {wait_time:.2f}s...")
                    time.sleep(wait_time)
                else:
                    time.sleep(random.uniform(2.0, 5.0))

                response = self.client.get(url, headers=self.get_headers())
                
                if response.status_code == 429:
                    print(f"Received 429 Too Many Requests for {url}")
                    continue
                
                response.raise_for_status()
                return BeautifulSoup(response.text, 'html.parser')
            
            except httpx.HTTPStatusError as e:
                if i == retries - 1:
                    raise e
                print(f"HTTP error {e.response.status_code}, retrying...")
            except Exception as e:
                if i == retries - 1:
                    raise e
                print(f"Error fetching {url}: {e}, retrying...")
        
        raise Exception(f"Failed to fetch {url} after {retries} retries due to 429")

    def close(self):
        self.client.close()
