#!/usr/bin/env python3
"""
Run crawler to fetch latest articles.
Run: python scripts/run_crawler.py
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.database import AsyncSessionLocal
from app.services.crawler_service import crawler_service


async def run_crawler():
    """Run all crawlers and process articles."""
    print("=" * 50)
    print("AI News Crawler")
    print("=" * 50)
    
    async with AsyncSessionLocal() as session:
        # Run crawlers
        print("\n[1/2] Running crawlers...")
        stats = await crawler_service.crawl_all(session)
        print(f"  - Crawled: {stats['crawled']} articles")
        print(f"  - New: {stats['new']} articles")
        print(f"  - Errors: {stats['errors']}")
        
        # Process with AI
        print("\n[2/2] Processing with AI...")
        processed = await crawler_service.process_pending_articles(session, limit=50)
        print(f"  - Processed: {processed} articles")
    
    print("\n" + "=" * 50)
    print("Done!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(run_crawler())
