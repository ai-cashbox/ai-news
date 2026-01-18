<p align="center">
  <img src="docs/assets/logo.svg" alt="AI News Logo" width="120" height="120">
</p>

<h1 align="center">AI News Hub</h1>

<p align="center">
  <strong>The AI-Powered News Aggregator</strong><br>
  Discover, Filter, and Understand AI News — Intelligence for the Intelligent
</p>

<p align="center">
  <a href="https://github.com/ai-news/ai-news/actions"><img src="https://img.shields.io/github/actions/workflow/status/ai-news/ai-news/ci.yml?branch=main&style=flat-square" alt="Build Status"></a>
  <a href="https://github.com/ai-news/ai-news/releases"><img src="https://img.shields.io/github/v/release/ai-news/ai-news?style=flat-square" alt="Release"></a>
  <a href="https://codecov.io/gh/ai-news/ai-news"><img src="https://img.shields.io/codecov/c/github/ai-news/ai-news?style=flat-square" alt="Coverage"></a>
  <a href="https://github.com/ai-news/ai-news/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ai-news/ai-news?style=flat-square" alt="License"></a>
  <a href="https://discord.gg/ainews"><img src="https://img.shields.io/discord/123456789?style=flat-square&logo=discord" alt="Discord"></a>
</p>

<p align="center">
  <a href="https://ainewshub.dev">Website</a> •
  <a href="https://docs.ainewshub.dev">Documentation</a> •
  <a href="https://ainewshub.dev/subscribe">Subscribe</a> •
  <a href="https://discord.gg/ainews">Discord</a> •
  <a href="https://twitter.com/ainewshub">Twitter</a>
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="README.zh-CN.md">简体中文</a>
</p>

---

## What is AI News Hub?

**AI News Hub** is an open-source, AI-powered news aggregation platform that automatically collects, evaluates, summarizes, and delivers the most important AI news from around the world. Think of it as your **personal AI research assistant** that reads thousands of articles so you don't have to.

```bash
# Get today's top AI news via API
curl https://api.ainewshub.dev/v1/articles/today?limit=10

# Subscribe to daily digest
curl -X POST https://api.ainewshub.dev/v1/subscribe \
  -d '{"email": "your@email.com", "frequency": "daily"}'
```

### Why AI News Hub?

The AI landscape is evolving rapidly, but staying informed is increasingly difficult:

| Problem | AI News Hub Solution |
|---------|---------------------|
| Information overload | **AI-powered quality scoring** filters the noise |
| Scattered sources | **Unified aggregation** from 50+ authoritative sources |
| Language barriers | **Automatic translation** with terminology preservation |
| Complex papers | **Plain-language summaries** for any audience |
| Manual curation | **Personalized recommendations** based on interests |
| Delayed discovery | **Real-time monitoring** of breaking developments |

## Features

- **Smart Aggregation** — Automatic collection from arXiv, tech blogs, Twitter/X, GitHub Trending
- **Quality Scoring** — Transparent algorithm evaluating source authority, content depth, and impact
- **AI Summarization** — 3-sentence summaries: What it is, Why it matters, What's the impact
- **Auto Translation** — Seamless Chinese-English bilingual support
- **Personalization** — Customize by category (LLM, CV, Agents, etc.) and quality threshold
- **Multi-Channel Delivery** — Web, Email, RSS, API, WeChat (coming soon)
- **AI Q&A** — Ask questions about recent AI developments
- **Self-Hostable** — Deploy your own instance with full control

## Quick Start

### Docker Deployment (Recommended)

```bash
# Clone the repository
git clone https://github.com/ai-news/ai-news.git
cd ai-news

# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# Start all services
docker-compose up -d

# Initialize sample data
docker-compose exec backend python scripts/init_db.py

# Run your first crawl
docker-compose exec backend python scripts/run_crawler.py
```

### Local Development

```bash
# Prerequisites: Python 3.11+, Node.js 20+, PostgreSQL 15+, Redis 7+

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev

# Access
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Makefile Commands

```bash
make dev        # Start development environment
make test       # Run all tests
make crawl      # Run crawlers manually
make process    # Process articles with AI
make email      # Send daily digest
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AI News Hub Platform                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐          │
│   │   Web UI    │     │  REST API   │     │  Scheduler  │          │
│   │  (Next.js)  │     │  (FastAPI)  │     │   (Cron)    │          │
│   └──────┬──────┘     └──────┬──────┘     └──────┬──────┘          │
│          │                   │                   │                  │
│          └───────────────────┼───────────────────┘                  │
│                              │                                       │
│   ┌──────────────────────────┴──────────────────────────┐           │
│   │                    Core Services                     │           │
│   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │           │
│   │  │ Crawler  │ │    AI    │ │  Email   │ │  Auth  │ │           │
│   │  │ Service  │ │Processor │ │ Service  │ │Service │ │           │
│   │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │           │
│   └──────────────────────────┬──────────────────────────┘           │
│                              │                                       │
│   ┌──────────────────────────┴──────────────────────────┐           │
│   │                   Data Sources                       │           │
│   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │           │
│   │  │  arXiv   │ │TechCrunch│ │The Verge │ │ GitHub │ │           │
│   │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │           │
│   └──────────────────────────┬──────────────────────────┘           │
│                              │                                       │
│   ┌──────────────────────────┴──────────────────────────┐           │
│   │                   Infrastructure                     │           │
│   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │           │
│   │  │PostgreSQL│ │  Redis   │ │LLM (GPT/ │ │ Vector │ │           │
│   │  │          │ │          │ │ Claude)  │ │   DB   │ │           │
│   │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │           │
│   └─────────────────────────────────────────────────────┘           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
ai-news/
├── backend/                     # Python FastAPI Backend
│   ├── app/
│   │   ├── api/                # REST API endpoints
│   │   │   ├── articles.py     # Article CRUD & search
│   │   │   ├── users.py        # Authentication & users
│   │   │   └── admin.py        # Admin operations
│   │   ├── models/             # SQLAlchemy models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business logic
│   │   │   ├── crawler/        # Data crawlers
│   │   │   │   ├── arxiv.py    # arXiv paper crawler
│   │   │   │   ├── techcrunch.py
│   │   │   │   └── theverge.py
│   │   │   ├── ai_processor.py # AI summarization & scoring
│   │   │   └── email_service.py
│   │   ├── config.py           # Configuration
│   │   ├── database.py         # Database setup
│   │   └── main.py             # Application entry
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                    # Next.js Frontend
│   ├── src/
│   │   ├── app/                # App router pages
│   │   │   ├── page.tsx        # Homepage (Today's picks)
│   │   │   ├── articles/       # All articles
│   │   │   ├── login/          # Authentication
│   │   │   └── settings/       # User preferences
│   │   ├── components/         # React components
│   │   └── lib/                # Utilities & API client
│   ├── package.json
│   └── Dockerfile
│
├── scripts/                     # Utility scripts
│   ├── init_db.py              # Database initialization
│   └── run_crawler.py          # Manual crawler trigger
│
├── docs/                        # Documentation
├── docker-compose.yml
└── Makefile
```

## API Reference

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register` | POST | Register a new user |
| `/api/v1/auth/login` | POST | Login and get JWT token |
| `/api/v1/auth/me` | GET | Get current user profile |

### Articles

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/articles` | GET | List articles with filters |
| `/api/v1/articles/today` | GET | Get today's top picks |
| `/api/v1/articles/{id}` | GET | Get article details |
| `/api/v1/articles/search` | GET | Full-text search |
| `/api/v1/articles/ask` | POST | AI Q&A about recent news |

### Subscriptions

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/subscriptions` | GET | Get user subscriptions |
| `/api/v1/subscriptions` | POST | Create subscription |
| `/api/v1/subscriptions/{id}` | PUT | Update subscription |

### Admin

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/admin/crawl` | POST | Trigger crawler manually |
| `/api/v1/admin/process` | POST | Trigger AI processing |
| `/api/v1/admin/email` | POST | Send digest emails |

### Example Request

```bash
# Get today's articles, filtered by category
curl "https://api.ainewshub.dev/v1/articles/today?category=llm&min_score=70"

# Response
{
  "data": [
    {
      "id": "abc123",
      "title": "GPT-5 Released: 300% Improvement in Reasoning",
      "summary": "OpenAI releases GPT-5 with breakthrough reasoning capabilities...",
      "source": "OpenAI Blog",
      "quality_score": 95,
      "category": "llm",
      "published_at": "2026-01-17T10:00:00Z",
      "url": "https://openai.com/blog/gpt-5"
    }
  ],
  "total": 42,
  "page": 1
}
```

## Quality Scoring Algorithm

Our transparent scoring system helps you identify the most valuable content:

```
Total Score = Source Authority (30%) 
            + Content Depth (25%) 
            + Timeliness (20%) 
            + Community Signal (15%) 
            + Originality (10%)

Source Authority:
  • Top Conferences / Official Blogs: 90-100
  • Major Tech Media: 70-85  
  • Personal Blogs / Twitter: 40-60 (adjusted by author influence)

Content Depth:
  • Technical analysis with code: 90-100
  • Detailed explanation: 70-85
  • News summary: 50-65
  • Brief mention: 30-45
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `OPENAI_API_KEY` | OpenAI API key for summarization | - |
| `ANTHROPIC_API_KEY` | Claude API key (alternative) | - |
| `JWT_SECRET` | Secret for JWT token signing | - |
| `SMTP_HOST` | SMTP server for emails | - |
| `SMTP_PORT` | SMTP port | `587` |
| `SMTP_USER` | SMTP username | - |
| `SMTP_PASSWORD` | SMTP password | - |
| `CRAWLER_INTERVAL` | Crawl interval in minutes | `60` |

## Adding New Data Sources

Extend the crawler system by implementing the `BaseCrawler` interface:

```python
# backend/app/services/crawler/my_source.py
from .base import BaseCrawler, RawArticle

class MySourceCrawler(BaseCrawler):
    name = "my_source"
    base_url = "https://example.com"
    
    async def crawl(self) -> list[RawArticle]:
        # Implement your crawling logic
        articles = []
        # ... fetch and parse articles
        return articles
```

Register in `crawler_service.py`:

```python
from .crawler.my_source import MySourceCrawler

CRAWLERS = [
    ArxivCrawler(),
    TechCrunchCrawler(),
    MySourceCrawler(),  # Add here
]
```

## Development

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

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

### Code Style

```bash
# Python
cd backend
black .
isort .
flake8 .
mypy app/

# TypeScript
cd frontend
npm run lint
npm run format
```

## Roadmap

### Released
- [x] Core crawlers (arXiv, TechCrunch, The Verge)
- [x] AI summarization & quality scoring
- [x] Web frontend MVP
- [x] User authentication
- [x] Email subscription

### In Progress
- [ ] GitHub Trending integration
- [ ] Twitter/X AI influencer tracking
- [ ] Chinese source integration (机器之心, etc.)

### Planned
- [ ] Mobile app (React Native)
- [ ] WeChat mini-program
- [ ] Browser extension
- [ ] Slack/Discord bots
- [ ] Vector search for semantic queries
- [ ] Multi-language support
- [ ] Premium features & API tiers

See our [public roadmap](https://github.com/ai-news/ai-news/projects/1) for details.

## Contributing

We welcome contributions! Please read our [Contributing Guide](CONTRIBUTING.md) before submitting a Pull Request.

### Ways to Contribute

- **Report bugs** — File an issue describing the bug
- **Suggest features** — Open a discussion for new ideas
- **Submit PRs** — Fix bugs or implement features
- **Add crawlers** — Integrate new data sources
- **Improve docs** — Fix typos or clarify documentation
- **Translate** — Help with i18n

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Community

- **Discord** — [Join our Discord server](https://discord.gg/ainews) for discussions
- **Twitter** — Follow [@ainewshub](https://twitter.com/ainewshub) for updates
- **GitHub Discussions** — [Ask questions](https://github.com/ai-news/ai-news/discussions)

## Security

If you discover a security vulnerability, please send an email to security@ainewshub.dev. Do not open a public issue.

See [SECURITY.md](SECURITY.md) for our security policy.

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by [Hacker News](https://news.ycombinator.com), [TLDR AI](https://tldr.tech/ai), and [The Rundown AI](https://therundown.ai)
- Built with [FastAPI](https://fastapi.tiangolo.com), [Next.js](https://nextjs.org), and [Tailwind CSS](https://tailwindcss.com)
- AI powered by [OpenAI](https://openai.com) and [Anthropic](https://anthropic.com)
- Thanks to all [contributors](https://github.com/ai-news/ai-news/graphs/contributors)

---

<p align="center">
  <sub>Built with ❤️ by the AI News Hub community</sub>
</p>
