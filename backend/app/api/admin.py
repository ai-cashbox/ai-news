from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database import get_db
from app.models.article import Article
from app.services.crawler_service import crawler_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/crawl")
async def trigger_crawl(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """Manually trigger a crawl job."""
    stats = await crawler_service.crawl_all(db)
    return {"message": "Crawl completed", "stats": stats}


@router.post("/process")
async def trigger_process(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """Manually trigger AI processing for pending articles."""
    processed = await crawler_service.process_pending_articles(db, limit)
    return {"message": "Processing completed", "processed": processed}


@router.get("/stats")
async def get_stats(
    db: AsyncSession = Depends(get_db),
):
    """Get system statistics."""
    # Total articles
    total_stmt = select(func.count(Article.id))
    total_result = await db.execute(total_stmt)
    total = total_result.scalar()
    
    # Processed articles
    processed_stmt = select(func.count(Article.id)).where(Article.is_processed == 1)
    processed_result = await db.execute(processed_stmt)
    processed = processed_result.scalar()
    
    # Pending articles
    pending_stmt = select(func.count(Article.id)).where(Article.is_processed == 0)
    pending_result = await db.execute(pending_stmt)
    pending = pending_result.scalar()
    
    # Average quality score
    avg_stmt = select(func.avg(Article.quality_score)).where(Article.is_processed == 1)
    avg_result = await db.execute(avg_stmt)
    avg_score = avg_result.scalar() or 0
    
    return {
        "total_articles": total,
        "processed_articles": processed,
        "pending_articles": pending,
        "average_quality_score": round(avg_score, 2),
    }
