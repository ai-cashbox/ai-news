from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from typing import Optional, List
from app.database import get_db
from app.models.article import Article, ArticleSource, ArticleCategory
from app.schemas.article import ArticleResponse, ArticleListResponse

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=ArticleListResponse)
async def get_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    source: Optional[str] = None,
    min_score: int = Query(0, ge=0, le=100),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get paginated list of articles."""
    # Build query
    conditions = [Article.is_processed == 1]
    
    if category:
        try:
            cat_enum = ArticleCategory(category)
            conditions.append(Article.category == cat_enum)
        except ValueError:
            pass
    
    if source:
        try:
            src_enum = ArticleSource(source)
            conditions.append(Article.source == src_enum)
        except ValueError:
            pass
    
    if min_score > 0:
        conditions.append(Article.quality_score >= min_score)
    
    if search:
        search_pattern = f"%{search}%"
        conditions.append(
            (Article.title.ilike(search_pattern)) | 
            (Article.title_zh.ilike(search_pattern)) |
            (Article.summary.ilike(search_pattern))
        )
    
    # Count total
    count_stmt = select(func.count(Article.id)).where(and_(*conditions))
    total_result = await db.execute(count_stmt)
    total = total_result.scalar()
    
    # Get paginated results
    offset = (page - 1) * page_size
    stmt = (
        select(Article)
        .where(and_(*conditions))
        .order_by(desc(Article.quality_score), desc(Article.published_at))
        .offset(offset)
        .limit(page_size)
    )
    
    result = await db.execute(stmt)
    articles = result.scalars().all()
    
    return ArticleListResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[ArticleResponse.model_validate(a) for a in articles],
    )


@router.get("/today", response_model=List[ArticleResponse])
async def get_today_articles(
    limit: int = Query(10, ge=1, le=50),
    min_score: int = Query(60, ge=0, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get today's top articles."""
    from datetime import datetime, timedelta
    
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    stmt = (
        select(Article)
        .where(
            and_(
                Article.is_processed == 1,
                Article.quality_score >= min_score,
                Article.crawled_at >= today - timedelta(days=1),
            )
        )
        .order_by(desc(Article.quality_score))
        .limit(limit)
    )
    
    result = await db.execute(stmt)
    articles = result.scalars().all()
    
    return [ArticleResponse.model_validate(a) for a in articles]


@router.get("/categories")
async def get_categories():
    """Get all available categories."""
    return [
        {"value": c.value, "label": c.value.upper().replace("_", " ")}
        for c in ArticleCategory
    ]


@router.get("/sources")
async def get_sources():
    """Get all available sources."""
    return [
        {"value": s.value, "label": s.value.replace("_", " ").title()}
        for s in ArticleSource
    ]


@router.get("/{article_id}", response_model=ArticleResponse)
async def get_article(
    article_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a single article by ID."""
    stmt = select(Article).where(Article.id == article_id)
    result = await db.execute(stmt)
    article = result.scalar_one_or_none()
    
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    return ArticleResponse.model_validate(article)
