import feedparser
from typing import List, Dict, Any
from datetime import datetime
import re
from app.services.crawler.base import BaseCrawler
from app.models.article import ArticleSource


class ArxivCrawler(BaseCrawler):
    """Crawler for arXiv AI papers."""
    
    # arXiv categories related to AI
    CATEGORIES = [
        "cs.AI",   # Artificial Intelligence
        "cs.CL",   # Computation and Language (NLP)
        "cs.CV",   # Computer Vision
        "cs.LG",   # Machine Learning
        "cs.NE",   # Neural and Evolutionary Computing
        "cs.RO",   # Robotics
    ]
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def get_source_name(self) -> str:
        return ArticleSource.ARXIV.value
    
    async def crawl(self, max_results: int = 50) -> List[Dict[str, Any]]:
        """Crawl recent arXiv papers."""
        articles = []
        
        # Build query for AI-related categories
        cat_query = " OR ".join([f"cat:{cat}" for cat in self.CATEGORIES])
        query = f"({cat_query})"
        
        url = f"{self.BASE_URL}?search_query={query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
        
        xml_content = await self.fetch_xml(url, timeout=60.0)
        if not xml_content:
            return articles
        
        feed = feedparser.parse(xml_content)
        
        for entry in feed.entries:
            try:
                article = self._parse_entry(entry)
                if article:
                    articles.append(article)
            except Exception as e:
                print(f"Error parsing arXiv entry: {e}")
                continue
        
        return articles
    
    def _parse_entry(self, entry: Dict) -> Dict[str, Any]:
        """Parse a single arXiv entry."""
        # Extract arXiv ID
        arxiv_id = entry.get("id", "").split("/abs/")[-1]
        
        # Get PDF and abstract page URLs
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
        abs_url = f"https://arxiv.org/abs/{arxiv_id}"
        
        # Parse authors
        authors = []
        for author in entry.get("authors", []):
            name = author.get("name", "")
            if name:
                authors.append(name)
        
        # Parse published date
        published_str = entry.get("published", "")
        published_at = None
        if published_str:
            try:
                published_at = datetime.fromisoformat(published_str.replace("Z", "+00:00"))
            except ValueError:
                pass
        
        # Get categories/tags
        tags = []
        for tag in entry.get("tags", []):
            term = tag.get("term", "")
            if term:
                tags.append(term)
        
        # Clean summary (abstract)
        summary = entry.get("summary", "")
        summary = re.sub(r'\s+', ' ', summary).strip()
        
        return {
            "title": entry.get("title", "").replace("\n", " ").strip(),
            "url": abs_url,
            "content": summary,
            "authors": authors,
            "tags": tags,
            "published_at": published_at,
            "source": self.get_source_name(),
        }
