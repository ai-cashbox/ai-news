from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=True)
    
    # Preferences
    preferred_categories = Column(JSON, default=list)  # List of ArticleCategory
    preferred_sources = Column(JSON, default=list)  # List of ArticleSource
    min_quality_score = Column(Integer, default=60)  # Minimum quality score to show
    
    # Email preferences
    email_frequency = Column(String(20), default="daily")  # daily, weekly, realtime
    email_enabled = Column(Boolean, default=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    subscriptions = relationship("Subscription", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.id}: {self.email}>"
