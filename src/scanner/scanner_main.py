import argparse
import requests
from bs4 import BeautifulSoup
import json
import os
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import urlparse, urljoin, urlunparse
from pathlib import Path


class RequestHandler:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RequestHandler, cls).__new__(cls)
            cls._instance.session = requests.Session()
            retries = Retry(total=5, backoff_factor=10, status_forcelist=[502, 503, 504])
            cls._instance.session.mount('http://', HTTPAdapter(max_retries=retries))
            cls._instance.session.mount('https://', HTTPAdapter(max_retries=retries))
            cls._instance.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
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
    def __init__(self, subdomain: str, output_dir: Path, debug=True):
        self.visited_urls = set()
        self.skipped_urls = set()
        self.request_handler = RequestHandler()
        self.output_dir = output_dir
        self.domain = subdomain   # any subsequent URLs must contain this domain to avoid scraping the entire website / external links
        self.debug = debug
        os.makedirs(self.output_dir, exist_ok=True)

    def normalize_url(self, url):
        parsed_url = urlparse(url)
        # Remove fragment and normalize path
        normalized_url = urlunparse(parsed_url._replace(fragment='', path=parsed_url.path.rstrip('/')))
        return normalized_url

    def scrape_page(self, url):
        url = self.normalize_url(url)
        if url in self.visited_urls:
            return
        self.visited_urls.add(url)

        # Skip mailto links
        if url.startswith("mailto:"):
            if link not in self.skipped_urls:
                self.skipped_urls.add(link)
                print("SKIPPED LINK:", link)
            return

        # Fetch the webpage content
        response = self.request_handler.get(url)
        if response is None:
            if link not in self.skipped_urls:
                self.skipped_urls.add(link)
                print("EMPTY LINK:", link)           
            return

        print(f"{url} ...")
        
        web_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(web_content, 'html.parser')

        # Extract relevant data while avoiding ads
        data = {
            "url": url,
            "title": soup.title.string if soup.title else '',
            "headings": [h.get_text() for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])],
            "paragraphs": [p.get_text() for p in soup.find_all('p') if not self.is_ad(p)],
            "links": [urljoin(url, a['href']) for a in soup.find_all('a', href=True) if not self.is_ad(a)]
        }

        # Store the extracted data in a JSON file
        filename = self.output_dir / f"scraped_data_{len(self.visited_urls)}.json"
        # with open(filename, 'w', encoding="utf-8-sig") as f:
        #     json.dump(data, f, indent=4 if self.debug else None, ensure_ascii=False)

        # Recursively scrape the links
        for link in data["links"]:
            # the link must contain the subdomain to avoid scraping the entire website
            if self.domain in link:
                self.scrape_page(link)
            else:
                if link not in self.skipped_urls:
                    self.skipped_urls.add(link)
                    print("SKIPPED LINK:", link)

    def is_ad(self, element):
        """Check if an element is likely an ad based on its attributes."""
        ad_keywords = ['ad', 'advertisement', 'sponsored']
        return any(keyword in element.get('class', []) for keyword in ad_keywords)
   

if __name__ == "__main__":
    # parent_subdomain = "https://www.ign.com/wikis/baldurs-gate-3"  # filter out URLs that don't contain this substring to avoid scraping the entire website / external links / ads
    # parent_url = "https://www.ign.com/wikis/baldurs-gate-3/Walkthrough"  # start scraping from this URL

    # get the project's parent directory
    # project_dir = Path(__file__).resolve().parents[1]
    # output_dir = project_dir / 'raw-output'
    # scraper = WebScraper(parent_subdomain, output_dir)
    # scraper.scrape_page(parent_url)

    parser = argparse.ArgumentParser(description="Web scraper for extracting data from a website.")
    # parser.add_argument("--subdomain", type=str, default='https://www.thegamer.com/baldurs-gate-3', help="Stay within this subdomain when scraping.")
    # parser.add_argument("--parent_url", type=str, default='https://www.thegamer.com/baldurs-gate-3-bg3-complete-guide-walkthrough', help="The URL to start scraping from.")
    # parser.add_argument("--output_dir", type=Path, default=r'/workspaces/guidescanner/data/scraped_websites/bg3_thegamer.com', help="The directory to save the scraped data.")
    parser.add_argument("--subdomain", type=str, default='https://www.ign.com/wikis/baldurs-gate-3', help="Stay within this subdomain when scraping.")
    parser.add_argument("--parent_url", type=str, default='https://www.ign.com/wikis/baldurs-gate-3/Walkthrough', help="The URL to start scraping from.")
    parser.add_argument("--output_dir", type=Path, default=r'/workspaces/guidescanner/data/scraped_websites/bg3_ign_v2', help="The directory to save the scraped data.")

    parser.add_argument("--debug", action="store_true", default=True, help="Enable debug mode for detailed output.")
    args = parser.parse_args()
    output_dir = Path(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    scraper = WebScraper(args.subdomain, output_dir, args.debug)
    scraper.scrape_page(args.parent_url)


    # maybe try this one:
    # https://baldursgate3.wiki.fextralife.com/Walkthrough
