import requests
from bs4 import BeautifulSoup
from newspaper import Article
from typing import List, Dict
import time
import logging
from urllib.parse import urlparse
import re
import aiohttp
import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import os

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.setup_logging()
        self.setup_cache()
        self.executor = ThreadPoolExecutor(max_workers=5)

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)

    def setup_cache(self):
        """Setup local cache for scraped content."""
        self.cache_dir = "data/cache"
        os.makedirs(self.cache_dir, exist_ok=True)

    def get_cache_path(self, url: str) -> str:
        """Get cache file path for a URL."""
        url_hash = hash(url)
        return os.path.join(self.cache_dir, f"{url_hash}.json")

    def load_from_cache(self, url: str) -> Dict:
        """Load content from cache if available."""
        cache_path = self.get_cache_path(url)
        if os.path.exists(cache_path):
            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_to_cache(self, url: str, content: Dict):
        """Save content to cache."""
        cache_path = self.get_cache_path(url)
        with open(cache_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False)

    def is_valid_url(self, url: str) -> bool:
        """Check if the URL is valid and accessible."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False

    def clean_text(self, text: str) -> str:
        """Clean the scraped text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()

    async def fetch_url(self, session: aiohttp.ClientSession, url: str) -> str:
        """Fetch URL content asynchronously."""
        try:
            async with session.get(url, headers=self.headers) as response:
                return await response.text()
        except Exception as e:
            self.logger.error(f"Error fetching {url}: {str(e)}")
            return ""

    async def scrape_article_async(self, url: str) -> Dict:
        """Scrape a single article asynchronously."""
        # Check cache first
        cached_content = self.load_from_cache(url)
        if cached_content:
            return cached_content

        try:
            async with aiohttp.ClientSession() as session:
                html = await self.fetch_url(session, url)
                if not html:
                    return None

                article = Article(url)
                article.set_html(html)
                article.parse()
                article.nlp()

                content = {
                    'title': article.title,
                    'text': self.clean_text(article.text),
                    'summary': article.summary,
                    'keywords': article.keywords,
                    'url': url,
                    'publish_date': article.publish_date,
                    'authors': article.authors
                }

                # Save to cache
                self.save_to_cache(url, content)
                return content

        except Exception as e:
            self.logger.error(f"Error scraping {url}: {str(e)}")
            return None

    def search_duckduckgo(self, query: str, num_results: int = 10) -> List[str]:
        """Search DuckDuckGo for relevant URLs (free alternative to Google)."""
        try:
            # Using DuckDuckGo's HTML interface
            search_url = f"https://html.duckduckgo.com/html/?q={query}"
            response = requests.get(search_url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            urls = []
            for result in soup.find_all('a', class_='result__url'):
                url = result.get('href')
                if url and url.startswith('http'):
                    urls.append(url)
            
            return urls[:num_results]
        except Exception as e:
            self.logger.error(f"Error searching DuckDuckGo: {str(e)}")
            return []

    def get_academic_sources(self) -> List[str]:
        """Get list of free academic sources."""
        return [
            "arxiv.org",
            "sci-hub.se",
            "core.ac.uk",
            "unpaywall.org",
            "doaj.org"
        ]

    def get_news_sources(self) -> List[str]:
        """Get list of free news sources."""
        return [
            "reuters.com",
            "apnews.com",
            "bbc.com",
            "theguardian.com",
            "aljazeera.com"
        ]

    async def scrape_multiple_sources(self, query: str, num_sources: int = 5) -> List[Dict]:
        """Scrape multiple sources for a given query asynchronously."""
        # Get URLs from DuckDuckGo
        urls = self.search_duckduckgo(query, num_sources)
        
        # Add academic and news sources
        academic_sources = self.get_academic_sources()
        news_sources = self.get_news_sources()
        
        # Create tasks for async scraping
        tasks = []
        async with aiohttp.ClientSession() as session:
            for url in urls:
                if self.is_valid_url(url):
                    tasks.append(self.scrape_article_async(url))
            
            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks)
        
        # Filter out None results
        return [r for r in results if r is not None]

    def get_relevant_sources(self, query: str) -> List[str]:
        """Get a list of relevant sources based on the query."""
        # Combine all available free sources
        return (
            self.get_academic_sources() +
            self.get_news_sources() +
            ["wikipedia.org", "britannica.com"]
        ) 