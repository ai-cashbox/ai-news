# Contributing to AI News Hub

First off, thank you for considering contributing to AI News Hub! It's people like you that make AI News Hub such a great tool for the AI community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guides](#style-guides)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Issues

- **Bug Reports**: If you find a bug, please create an issue using the bug report template
- **Feature Requests**: Have an idea? Open an issue using the feature request template
- **Questions**: Use GitHub Discussions for questions

### Good First Issues

Looking for a place to start? Check out issues labeled [`good first issue`](https://github.com/ai-news/ai-news/labels/good%20first%20issue).

## How Can I Contribute?

### 1. Code Contributions

- Fix bugs
- Implement new features
- Add new data source crawlers
- Improve AI processing algorithms
- Write tests
- Optimize performance

### 2. Non-Code Contributions

- Report bugs
- Suggest features
- Improve documentation
- Help other users
- Spread the word
- Translate to other languages

### 3. Data Source Contributions

- Identify authoritative AI news sources
- Implement new crawlers
- Improve data quality algorithms
- Test and validate data accuracy

## Development Setup

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### Clone and Setup

```bash
# Clone the repository
git clone https://github.com/ai-news/ai-news.git
cd ai-news

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration

# Start infrastructure
docker-compose up -d postgres redis

# Run database migrations
python scripts/init_db.py

# Start the backend
uvicorn app.main:app --reload --port 8000

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

### Running Tests

```bash
# Backend tests
cd backend
pytest --cov=app tests/

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
```

## Pull Request Process

### 1. Before You Start

- Check existing issues and PRs to avoid duplicate work
- For major changes, open an issue first to discuss

### 2. Branch Naming

```
feature/short-description
fix/issue-number-description
docs/what-you-documented
refactor/what-you-refactored
crawler/source-name
```

### 3. Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add GitHub Trending crawler
fix: resolve email sending issue
docs: update API documentation
refactor: simplify AI processor logic
test: add crawler unit tests
chore: update dependencies
crawler: add 机器之心 source
```

### 4. PR Checklist

- [ ] Code follows the style guidelines
- [ ] Self-reviewed the code
- [ ] Added/updated tests
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Related issues linked

### 5. Review Process

1. Submit PR
2. Automated checks run (CI, linting, tests)
3. Maintainer reviews
4. Address feedback
5. Approval and merge

## Style Guides

### Python Style Guide

- Follow [PEP 8](https://pep8.org/)
- Use `black` for formatting
- Use `isort` for import sorting
- Use type hints

```python
# Good
async def get_articles(
    category: str | None = None,
    min_score: int = 0,
    limit: int = 20,
) -> list[Article]:
    """Fetch articles with optional filters."""
    query = select(Article).where(Article.quality_score >= min_score)
    if category:
        query = query.where(Article.category == category)
    return await db.execute(query.limit(limit))

# Avoid
def get_articles(category, min_score, limit):
    # Missing type hints and docstring
    pass
```

### TypeScript/React Style Guide

- Use TypeScript strict mode
- Prefer functional components with hooks
- Use ESLint and Prettier

```tsx
// Good
interface ArticleCardProps {
  article: Article;
  onSelect?: (article: Article) => void;
}

export function ArticleCard({ article, onSelect }: ArticleCardProps) {
  return (
    <div onClick={() => onSelect?.(article)}>
      <h3>{article.title}</h3>
      <span className="score">{article.quality_score}</span>
    </div>
  );
}
```

### Crawler Implementation Guide

When adding a new data source crawler:

```python
# backend/app/services/crawler/my_source.py
from .base import BaseCrawler, RawArticle
from typing import List

class MySourceCrawler(BaseCrawler):
    """Crawler for MySource.com AI news."""
    
    name = "my_source"
    base_url = "https://mysource.com"
    authority_score = 75  # 0-100, based on source reputation
    
    async def crawl(self) -> List[RawArticle]:
        """
        Fetch and parse articles from the source.
        
        Returns:
            List of RawArticle objects with title, content, url, etc.
        """
        articles = []
        
        # 1. Fetch the page/API
        response = await self.fetch(f"{self.base_url}/ai-news")
        
        # 2. Parse the content
        items = self.parse_items(response)
        
        # 3. Transform to RawArticle format
        for item in items:
            articles.append(RawArticle(
                title=item.title,
                content=item.content,
                url=item.url,
                source=self.name,
                published_at=item.date,
            ))
        
        return articles
```

### Documentation Style

- Use clear, concise language
- Include code examples
- Keep README up to date
- Document all public APIs

## Project Structure

```
ai-news/
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # REST endpoints
│   │   ├── models/      # Database models
│   │   ├── schemas/     # Pydantic schemas
│   │   └── services/    # Business logic
│   │       └── crawler/ # Data crawlers
│   └── tests/
├── frontend/             # Next.js frontend
│   ├── src/
│   │   ├── app/         # Pages
│   │   ├── components/  # React components
│   │   └── lib/         # Utilities
│   └── __tests__/
├── scripts/              # Utility scripts
└── docs/                 # Documentation
```

## Community

- **Discord**: [Join our server](https://discord.gg/ainews)
- **Twitter**: [@ainewshub](https://twitter.com/ainewshub)
- **Discussions**: [GitHub Discussions](https://github.com/ai-news/ai-news/discussions)

## Recognition

Contributors are recognized in:
- README.md Contributors section
- Release notes
- Annual contributor spotlight

---

Thank you for contributing to AI News Hub! 🚀
