from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Enum as SQLEnum
from sqlalchemy.sql import func
from app.database import Base
import enum


class ArticleSource(str, enum.Enum):
    ARXIV = "arxiv"
    OPENAI_BLOG = "openai_blog"
    GOOGLE_AI_BLOG = "google_ai_blog"
    META_AI_BLOG = "meta_ai_blog"
    TECHCRUNCH = "techcrunch"
    THE_VERGE = "the_verge"
    JIQIZHIXIN = "jiqizhixin"  # 机器之心
    OTHER = "other"


class ArticleCategory(str, enum.Enum):
    LLM = "llm"
    MULTIMODAL = "multimodal"
    AGENT = "agent"
    CV = "cv"
    NLP = "nlp"
    RL = "rl"
    ROBOTICS = "robotics"
    AI_SAFETY = "ai_safety"
    BUSINESS = "business"
    OTHER = "other"


class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic info
    title = Column(String(500), nullable=False)
    title_zh = Column(String(500), nullable=True)  # Chinese translation
    url = Column(String(1000), unique=True, nullable=False)
    
    # Content
    content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)  # AI-generated summary
    summary_zh = Column(Text, nullable=True)  # Chinese summary
    
    # Metadata
    source = Column(SQLEnum(ArticleSource), default=ArticleSource.OTHER)
    category = Column(SQLEnum(ArticleCategory), default=ArticleCategory.OTHER)
    authors = Column(JSON, default=list)  # List of author names
    tags = Column(JSON, default=list)  # List of tags
    
    # Quality scoring
    quality_score = Column(Float, default=0.0)  # 0-100
    source_authority = Column(Float, default=0.0)  # 0-100
    content_depth = Column(Float, default=0.0)  # 0-100
    
    # Timestamps
    published_at = Column(DateTime(timezone=True), nullable=True)
    crawled_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Status
    is_processed = Column(Integer, default=0)  # 0: pending, 1: processed, -1: failed
    
    def __repr__(self):
        return f"<Article {self.id}: {self.title[:50]}>"
