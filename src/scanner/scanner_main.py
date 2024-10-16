import requests
from bs4 import BeautifulSoup
import json
import os
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import urlparse, urljoin
from pathlib import Path

class RequestHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RequestHandler, cls).__new__(cls)
            cls._instance.session = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
            cls._instance.session.mount('http://', HTTPAdapter(max_retries=retries))
            cls._instance.session.mount('https://', HTTPAdapter(max_retries=retries))
            cls._instance.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            })
            cls._instance.rate_limit_delay = 1  # seconds
        return cls._instance

    def get(self, url):
        time.sleep(self._instance.rate_limit_delay)
        try:
            response = self._instance.session.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None

class WebScraper:
    def __init__(self, parent_url: str, output_dir: Path, debug=True):
        self.visited_urls = set()
        self.request_handler = RequestHandler()
        self.output_dir = output_dir
        self.parent_url = parent_url
        self.domain = urlparse(parent_url).netloc
        self.debug = debug
        os.makedirs(self.output_dir, exist_ok=True)

    def scrape_page(self, url):
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)

        # Fetch the webpage content
        response = self.request_handler.get(url)
        if response is None:
            return
        web_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(web_content, 'html.parser')

        # Extract relevant data while avoiding ads
        data = {
            "url": url,
            "title": soup.title.string if soup.title else '',
            "headings": [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
            "paragraphs": [p.get_text() for p in soup.find_all('p') if not self.is_ad(p)],
            "links": [a['href'] for a in soup.find_all('a', href=True) if not self.is_ad(a)]
        }

        # Store the extracted data in a JSON file
        filename = self.output_dir / f"scraped_data_{len(self.visited_urls)}.json"
        with open(filename, 'w', encoding="utf-8-sig") as f:
            json.dump(data, f, indent=4 if self.debug else None, ensure_ascii=False)

        # Recursively follow links within the same domain
        for link in data['links']:
            full_link = urljoin(url, link)
            print(f"\r{full_link}", end=f"{' '*100}")

            if urlparse(full_link).netloc == self.domain and full_link.startswith(self.parent_url):
                self.scrape_page(full_link)

    def is_ad(self, element):
        """Check if an element is likely an ad based on its attributes."""
        ad_keywords = ['ad', 'advertisement', 'sponsored']
        return any(keyword in element.get('class', []) for keyword in ad_keywords)
    

if __name__ == "__main__":
    # parent_url = "https://gamerant.com/complete-guide-baldurs-gate-3-combat-quests-choices-companions-builds-classes-story-bg3"
    parent_subdomain = "https://www.ign.com/wikis/baldurs-gate-3"
    parent_url = "https://www.ign.com/wikis/baldurs-gate-3/Walkthrough"
    # get the project's parent directory
    project_dir = Path(__file__).resolve().parents[1]
    output_dir = project_dir / 'output'
    scraper = WebScraper(parent_subdomain, output_dir)
    scraper.scrape_page(parent_url)


