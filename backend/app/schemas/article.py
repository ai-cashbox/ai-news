from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime
from app.models.article import ArticleSource, ArticleCategory


class ArticleBase(BaseModel):
    title: str
    url: str
    source: ArticleSource = ArticleSource.OTHER
    category: ArticleCategory = ArticleCategory.OTHER


class ArticleCreate(ArticleBase):
    content: Optional[str] = None
    authors: List[str] = []
    tags: List[str] = []
    published_at: Optional[datetime] = None


class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    title_zh: Optional[str] = None
    content: Optional[str] = None
    summary: Optional[str] = None
    summary_zh: Optional[str] = None
    category: Optional[ArticleCategory] = None
    tags: Optional[List[str]] = None
    quality_score: Optional[float] = None
    source_authority: Optional[float] = None
    content_depth: Optional[float] = None
    is_processed: Optional[int] = None


class ArticleResponse(BaseModel):
    id: int
    title: str
    title_zh: Optional[str] = None
    url: str
    summary: Optional[str] = None
    summary_zh: Optional[str] = None
    source: ArticleSource
    category: ArticleCategory
    authors: List[str] = []
    tags: List[str] = []
    quality_score: float
    published_at: Optional[datetime] = None
    crawled_at: datetime
    
    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ArticleResponse]
