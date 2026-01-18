from typing import List, Optional
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.config import settings
from app.models.article import Article
from app.models.user import User
from app.models.subscription import Subscription


EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; margin-bottom: 20px; }
        .header h1 { margin: 0; font-size: 24px; }
        .header p { margin: 10px 0 0; opacity: 0.9; }
        .article { background: #f8f9fa; border-radius: 8px; padding: 20px; margin-bottom: 15px; border-left: 4px solid #667eea; }
        .article h2 { margin: 0 0 10px; font-size: 18px; }
        .article h2 a { color: #333; text-decoration: none; }
        .article h2 a:hover { color: #667eea; }
        .meta { font-size: 12px; color: #666; margin-bottom: 10px; }
        .score { display: inline-block; background: #667eea; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px; }
        .category { display: inline-block; background: #e9ecef; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-left: 5px; }
        .summary { color: #555; font-size: 14px; }
        .summary-zh { color: #777; font-size: 13px; margin-top: 8px; padding-top: 8px; border-top: 1px dashed #ddd; }
        .footer { text-align: center; color: #999; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; }
        .footer a { color: #667eea; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI News Daily</h1>
        <p>{{ date }} · {{ article_count }} 篇精选资讯</p>
    </div>
    
    {% for article in articles %}
    <div class="article">
        <h2><a href="{{ article.url }}" target="_blank">{{ article.title }}</a></h2>
        <div class="meta">
            <span class="score">⭐ {{ article.quality_score|int }}</span>
            <span class="category">{{ article.category }}</span>
            · {{ article.source }}
        </div>
        <div class="summary">{{ article.summary }}</div>
        {% if article.summary_zh %}
        <div class="summary-zh">{{ article.summary_zh }}</div>
        {% endif %}
    </div>
    {% endfor %}
    
    <div class="footer">
        <p>Powered by AI News Aggregator</p>
        <p><a href="#">取消订阅</a> · <a href="#">查看更多</a></p>
    </div>
</body>
</html>
"""


class EmailService:
    """Email notification service."""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.email_from = settings.EMAIL_FROM
        self.template = Template(EMAIL_TEMPLATE)
    
    async def send_daily_digest(self, db: AsyncSession) -> int:
        """Send daily digest to all subscribed users."""
        # Get users with daily email subscription
        stmt = select(User).where(
            and_(
                User.email_enabled == True,
                User.email_frequency == "daily",
                User.is_active == True,
            )
        )
        result = await db.execute(stmt)
        users = result.scalars().all()
        
        sent_count = 0
        
        for user in users:
            try:
                articles = await self._get_articles_for_user(db, user)
                if articles:
                    await self._send_digest_email(user, articles)
                    sent_count += 1
            except Exception as e:
                print(f"Error sending email to {user.email}: {e}")
        
        return sent_count
    
    async def _get_articles_for_user(
        self, 
        db: AsyncSession, 
        user: User, 
        hours: int = 24
    ) -> List[Article]:
        """Get relevant articles for a user."""
        since = datetime.utcnow() - timedelta(hours=hours)
        
        stmt = select(Article).where(
            and_(
                Article.is_processed == 1,
                Article.quality_score >= user.min_quality_score,
                Article.crawled_at >= since,
            )
        ).order_by(Article.quality_score.desc()).limit(10)
        
        result = await db.execute(stmt)
        return result.scalars().all()
    
    async def _send_digest_email(self, user: User, articles: List[Article]):
        """Send digest email to user."""
        if not self.smtp_user or not self.smtp_password:
            print(f"SMTP not configured, skipping email to {user.email}")
            return
        
        # Render email content
        html_content = self.template.render(
            date=datetime.now().strftime("%Y年%m月%d日"),
            article_count=len(articles),
            articles=[
                {
                    "title": a.title,
                    "url": a.url,
                    "summary": a.summary or "",
                    "summary_zh": a.summary_zh or "",
                    "quality_score": a.quality_score,
                    "category": a.category.value if a.category else "other",
                    "source": a.source.value if a.source else "unknown",
                }
                for a in articles
            ],
        )
        
        # Create email message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"🤖 AI News Daily - {datetime.now().strftime('%m/%d')}"
        msg["From"] = self.email_from
        msg["To"] = user.email
        
        msg.attach(MIMEText(html_content, "html", "utf-8"))
        
        # Send email
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)


# Singleton instance
email_service = EmailService()
