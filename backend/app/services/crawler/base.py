from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import httpx
from app.config import settings


class BaseCrawler(ABC):
    """Base class for all crawlers."""
    
    def __init__(self):
        self.headers = {
            "User-Agent": settings.CRAWLER_USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
    
    @abstractmethod
    async def crawl(self) -> List[Dict[str, Any]]:
        """Crawl and return a list of article data."""
        pass
    
    @abstractmethod
    def get_source_name(self) -> str:
        """Return the source name."""
        pass
    
    async def fetch_url(self, url: str, timeout: float = 30.0) -> Optional[str]:
        """Fetch content from URL."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=self.headers,
                    timeout=timeout,
                    follow_redirects=True,
                )
                if response.status_code == 200:
                    return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None
    
    async def fetch_xml(self, url: str, timeout: float = 30.0) -> Optional[str]:
        """Fetch XML/RSS content from URL."""
        headers = {**self.headers, "Accept": "application/xml,application/rss+xml,text/xml"}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url,
                    headers=headers,
                    timeout=timeout,
                    follow_redirects=True,
                )
                if response.status_code == 200:
                    return response.text
        except Exception as e:
            print(f"Error fetching XML {url}: {e}")
        return None
