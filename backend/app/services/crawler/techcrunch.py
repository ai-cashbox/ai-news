import feedparser
from typing import List, Dict, Any
from datetime import datetime
from bs4 import BeautifulSoup
import re
from app.services.crawler.base import BaseCrawler
from app.models.article import ArticleSource


class TechCrunchCrawler(BaseCrawler):
    """Crawler for TechCrunch AI articles."""
    
    RSS_URL = "https://techcrunch.com/category/artificial-intelligence/feed/"
    
    def get_source_name(self) -> str:
        return ArticleSource.TECHCRUNCH.value
    
    async def crawl(self, max_results: int = 30) -> List[Dict[str, Any]]:
        """Crawl TechCrunch AI articles via RSS."""
        articles = []
        
        xml_content = await self.fetch_xml(self.RSS_URL)
        if not xml_content:
            return articles
        
        feed = feedparser.parse(xml_content)
        
        for entry in feed.entries[:max_results]:
            try:
                article = self._parse_entry(entry)
                if article:
                    articles.append(article)
            except Exception as e:
                print(f"Error parsing TechCrunch entry: {e}")
                continue
        
        return articles
    
    def _parse_entry(self, entry: Dict) -> Dict[str, Any]:
        """Parse a single TechCrunch RSS entry."""
        # Get URL
        url = entry.get("link", "")
        if not url:
            return None
        
        # Parse authors
        authors = []
        if "author" in entry:
            authors.append(entry["author"])
        
        # Parse published date
        published_at = None
        if "published_parsed" in entry and entry["published_parsed"]:
            try:
                published_at = datetime(*entry["published_parsed"][:6])
            except (ValueError, TypeError):
                pass
        
        # Get content/summary
        content = ""
        if "content" in entry and entry["content"]:
            content = entry["content"][0].get("value", "")
        elif "summary" in entry:
            content = entry.get("summary", "")
        
        # Clean HTML from content
        if content:
            soup = BeautifulSoup(content, "html.parser")
            content = soup.get_text(separator=" ", strip=True)
            content = re.sub(r'\s+', ' ', content).strip()
        
        # Get tags
        tags = []
        for tag in entry.get("tags", []):
            term = tag.get("term", "")
            if term:
                tags.append(term)
        
        return {
            "title": entry.get("title", "").strip(),
            "url": url,
            "content": content,
            "authors": authors,
            "tags": tags,
            "published_at": published_at,
            "source": self.get_source_name(),
        }


class TheVergeCrawler(BaseCrawler):
    """Crawler for The Verge AI articles."""
    
    RSS_URL = "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"
    
    def get_source_name(self) -> str:
        return ArticleSource.THE_VERGE.value
    
    async def crawl(self, max_results: int = 30) -> List[Dict[str, Any]]:
        """Crawl The Verge AI articles via RSS."""
        articles = []
        
        xml_content = await self.fetch_xml(self.RSS_URL)
        if not xml_content:
            return articles
        
        feed = feedparser.parse(xml_content)
        
        for entry in feed.entries[:max_results]:
            try:
                article = self._parse_entry(entry)
                if article:
                    articles.append(article)
            except Exception as e:
                print(f"Error parsing The Verge entry: {e}")
                continue
        
        return articles
    
    def _parse_entry(self, entry: Dict) -> Dict[str, Any]:
        """Parse a single The Verge RSS entry."""
        url = entry.get("link", "")
        if not url:
            return None
        
        authors = []
        if "author" in entry:
            authors.append(entry["author"])
        
        published_at = None
        if "published_parsed" in entry and entry["published_parsed"]:
            try:
                published_at = datetime(*entry["published_parsed"][:6])
            except (ValueError, TypeError):
                pass
        
        content = entry.get("summary", "")
        if content:
            soup = BeautifulSoup(content, "html.parser")
            content = soup.get_text(separator=" ", strip=True)
        
        return {
            "title": entry.get("title", "").strip(),
            "url": url,
            "content": content,
            "authors": authors,
            "tags": [],
            "published_at": published_at,
            "source": self.get_source_name(),
        }
