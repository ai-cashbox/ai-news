from typing import List, Dict, Any
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.article import Article, ArticleSource, ArticleCategory
from app.services.crawler import ArxivCrawler, TechCrunchCrawler
from app.services.crawler.techcrunch import TheVergeCrawler
from app.services.ai_processor import ai_processor


class CrawlerService:
    """Service to manage all crawlers and process articles."""
    
    def __init__(self):
        self.crawlers = [
            ArxivCrawler(),
            TechCrunchCrawler(),
            TheVergeCrawler(),
        ]
    
    async def crawl_all(self, db: AsyncSession) -> Dict[str, int]:
        """Run all crawlers and save articles to database."""
        stats = {"crawled": 0, "new": 0, "errors": 0}
        
        for crawler in self.crawlers:
            try:
                articles = await crawler.crawl()
                stats["crawled"] += len(articles)
                
                for article_data in articles:
                    try:
                        saved = await self._save_article(db, article_data)
                        if saved:
                            stats["new"] += 1
                    except Exception as e:
                        print(f"Error saving article: {e}")
                        stats["errors"] += 1
                        
            except Exception as e:
                print(f"Error running crawler {crawler.get_source_name()}: {e}")
                stats["errors"] += 1
        
        await db.commit()
        return stats
    
    async def _save_article(self, db: AsyncSession, data: Dict[str, Any]) -> bool:
        """Save article to database if not exists."""
        # Check if article already exists
        stmt = select(Article).where(Article.url == data["url"])
        result = await db.execute(stmt)
        existing = result.scalar_one_or_none()
        
        if existing:
            return False
        
        # Create new article
        article = Article(
            title=data["title"],
            url=data["url"],
            content=data.get("content", ""),
            authors=data.get("authors", []),
            tags=data.get("tags", []),
            source=ArticleSource(data.get("source", "other")),
            published_at=data.get("published_at"),
            crawled_at=datetime.utcnow(),
            is_processed=0,
        )
        
        db.add(article)
        return True
    
    async def process_pending_articles(self, db: AsyncSession, limit: int = 20) -> int:
        """Process pending articles with AI."""
        # Get unprocessed articles
        stmt = select(Article).where(Article.is_processed == 0).limit(limit)
        result = await db.execute(stmt)
        articles = result.scalars().all()
        
        processed_count = 0
        
        for article in articles:
            try:
                # Process with AI
                ai_result = await ai_processor.process_article(
                    title=article.title,
                    content=article.content or "",
                    source=article.source.value if article.source else "other",
                )
                
                # Update article with AI results
                article.summary = ai_result.get("summary", "")
                article.summary_zh = ai_result.get("summary_zh", "")
                article.title_zh = ai_result.get("title_zh", "")
                article.quality_score = ai_result.get("quality_score", 50)
                article.content_depth = ai_result.get("content_depth", 50)
                article.source_authority = ai_result.get("source_authority", 50)
                
                # Set category
                category_str = ai_result.get("category", "other")
                try:
                    article.category = ArticleCategory(category_str)
                except ValueError:
                    article.category = ArticleCategory.OTHER
                
                # Update tags
                if ai_result.get("tags"):
                    article.tags = ai_result["tags"]
                
                article.is_processed = 1
                article.processed_at = datetime.utcnow()
                processed_count += 1
                
            except Exception as e:
                print(f"Error processing article {article.id}: {e}")
                article.is_processed = -1
        
        await db.commit()
        return processed_count


# Singleton instance
crawler_service = CrawlerService()
