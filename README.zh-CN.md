<p align="center">
  <img src="docs/assets/logo.svg" alt="AI News Logo" width="120" height="120">
</p>

<h1 align="center">AI News Hub</h1>

<p align="center">
  <strong>AI 驱动的资讯聚合平台</strong><br>
  发现、筛选、理解 AI 资讯 — 用 AI 筛选 AI 资讯
</p>

<p align="center">
  <a href="https://github.com/ai-news/ai-news/actions"><img src="https://img.shields.io/github/actions/workflow/status/ai-news/ai-news/ci.yml?branch=main&style=flat-square" alt="构建状态"></a>
  <a href="https://github.com/ai-news/ai-news/releases"><img src="https://img.shields.io/github/v/release/ai-news/ai-news?style=flat-square" alt="版本"></a>
  <a href="https://codecov.io/gh/ai-news/ai-news"><img src="https://img.shields.io/codecov/c/github/ai-news/ai-news?style=flat-square" alt="覆盖率"></a>
  <a href="https://github.com/ai-news/ai-news/blob/main/LICENSE"><img src="https://img.shields.io/github/license/ai-news/ai-news?style=flat-square" alt="许可证"></a>
  <a href="https://discord.gg/ainews"><img src="https://img.shields.io/discord/123456789?style=flat-square&logo=discord" alt="Discord"></a>
</p>

<p align="center">
  <a href="https://ainewshub.dev">官网</a> •
  <a href="https://docs.ainewshub.dev">文档</a> •
  <a href="https://ainewshub.dev/subscribe">订阅</a> •
  <a href="https://discord.gg/ainews">Discord</a> •
  <a href="https://twitter.com/ainewshub">Twitter</a>
</p>

<p align="center">
  <a href="README.md">English</a> | <strong>简体中文</strong>
</p>

---

## 什么是 AI News Hub？

**AI News Hub** 是一个开源的、AI 驱动的资讯聚合平台，它能自动采集、评估、摘要和推送全球最重要的 AI 资讯。你可以把它理解为你的 **个人 AI 研究助手**，它帮你阅读成千上万的文章，让你只看最有价值的内容。

```bash
# 通过 API 获取今日 AI 热点
curl https://api.ainewshub.dev/v1/articles/today?limit=10

# 订阅每日精选
curl -X POST https://api.ainewshub.dev/v1/subscribe \
  -d '{"email": "your@email.com", "frequency": "daily"}'
```

### 为什么需要 AI News Hub？

AI 领域发展迅猛，但保持信息同步越来越难：

| 痛点 | AI News Hub 解决方案 |
|------|---------------------|
| 信息过载 | **AI 质量评分** 过滤噪音 |
| 来源分散 | **统一聚合** 50+ 权威来源 |
| 语言障碍 | **自动翻译** 保留专业术语 |
| 论文晦涩 | **通俗摘要** 适合各类受众 |
| 人工筛选 | **个性化推荐** 基于兴趣定制 |
| 发现滞后 | **实时监控** 突发动态 |

## 核心特性

- **智能采集** — 自动从 arXiv、科技博客、Twitter/X、GitHub Trending 采集
- **质量评分** — 透明算法评估来源权威度、内容深度、影响力
- **AI 摘要** — 三句话摘要：是什么、为什么重要、影响是什么
- **自动翻译** — 无缝中英双语支持
- **个性化** — 按分类（LLM、CV、Agent 等）和质量阈值定制
- **多渠道推送** — Web、邮件、RSS、API、微信（即将上线）
- **AI 问答** — 询问近期 AI 动态
- **私有部署** — 部署自己的实例，完全掌控

## 快速开始

### Docker 部署（推荐）

```bash
# 克隆仓库
git clone https://github.com/ai-news/ai-news.git
cd ai-news

# 配置环境变量
cp backend/.env.example backend/.env
# 编辑 backend/.env 填入你的 API 密钥

# 启动所有服务
docker-compose up -d

# 初始化示例数据
docker-compose exec backend python scripts/init_db.py

# 运行第一次采集
docker-compose exec backend python scripts/run_crawler.py
```

### 本地开发

```bash
# 前置条件: Python 3.11+, Node.js 20+, PostgreSQL 15+, Redis 7+

# 后端设置
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000

# 前端设置（新终端）
cd frontend
npm install
npm run dev

# 访问地址
# 前端: http://localhost:3000
# 后端 API: http://localhost:8000
# API 文档: http://localhost:8000/docs
```

### Makefile 命令

```bash
make dev        # 启动开发环境
make test       # 运行所有测试
make crawl      # 手动运行爬虫
make process    # AI 处理文章
make email      # 发送每日精选
```

## 系统架构

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AI News Hub 平台                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐          │
│   │   Web 界面   │     │  REST API   │     │   定时任务   │          │
│   │  (Next.js)  │     │  (FastAPI)  │     │   (Cron)    │          │
│   └──────┬──────┘     └──────┬──────┘     └──────┬──────┘          │
│          │                   │                   │                  │
│          └───────────────────┼───────────────────┘                  │
│                              │                                       │
│   ┌──────────────────────────┴──────────────────────────┐           │
│   │                      核心服务                        │           │
│   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │           │
│   │  │ 爬虫服务  │ │  AI 处理 │ │ 邮件服务  │ │ 认证服务│ │           │
│   │  │ Crawler  │ │Processor │ │  Email   │ │  Auth  │ │           │
│   │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │           │
│   └──────────────────────────┬──────────────────────────┘           │
│                              │                                       │
│   ┌──────────────────────────┴──────────────────────────┐           │
│   │                      数据来源                        │           │
│   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │           │
│   │  │  arXiv   │ │TechCrunch│ │The Verge │ │ GitHub │ │           │
│   │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │           │
│   └──────────────────────────┬──────────────────────────┘           │
│                              │                                       │
│   ┌──────────────────────────┴──────────────────────────┐           │
│   │                      基础设施                        │           │
│   │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │           │
│   │  │PostgreSQL│ │  Redis   │ │LLM (GPT/ │ │ 向量库  │ │           │
│   │  │          │ │          │ │ Claude)  │ │        │ │           │
│   │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │           │
│   └─────────────────────────────────────────────────────┘           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## 项目结构

```
ai-news/
├── backend/                     # Python FastAPI 后端
│   ├── app/
│   │   ├── api/                # REST API 接口
│   │   │   ├── articles.py     # 文章增删改查 & 搜索
│   │   │   ├── users.py        # 认证 & 用户
│   │   │   └── admin.py        # 管理操作
│   │   ├── models/             # SQLAlchemy 模型
│   │   ├── schemas/            # Pydantic 模式
│   │   ├── services/           # 业务逻辑
│   │   │   ├── crawler/        # 数据爬虫
│   │   │   │   ├── arxiv.py    # arXiv 论文爬虫
│   │   │   │   ├── techcrunch.py
│   │   │   │   └── theverge.py
│   │   │   ├── ai_processor.py # AI 摘要 & 评分
│   │   │   └── email_service.py
│   │   ├── config.py           # 配置
│   │   ├── database.py         # 数据库设置
│   │   └── main.py             # 应用入口
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                    # Next.js 前端
│   ├── src/
│   │   ├── app/                # App 路由页面
│   │   │   ├── page.tsx        # 首页（今日精选）
│   │   │   ├── articles/       # 全部文章
│   │   │   ├── login/          # 认证
│   │   │   └── settings/       # 用户设置
│   │   ├── components/         # React 组件
│   │   └── lib/                # 工具 & API 客户端
│   ├── package.json
│   └── Dockerfile
│
├── scripts/                     # 工具脚本
│   ├── init_db.py              # 数据库初始化
│   └── run_crawler.py          # 手动触发爬虫
│
├── docs/                        # 文档
├── docker-compose.yml
└── Makefile
```

## API 参考

### 认证接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/v1/auth/register` | POST | 注册新用户 |
| `/api/v1/auth/login` | POST | 登录获取 JWT 令牌 |
| `/api/v1/auth/me` | GET | 获取当前用户信息 |

### 文章接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/v1/articles` | GET | 获取文章列表（带筛选） |
| `/api/v1/articles/today` | GET | 获取今日精选 |
| `/api/v1/articles/{id}` | GET | 获取文章详情 |
| `/api/v1/articles/search` | GET | 全文搜索 |
| `/api/v1/articles/ask` | POST | AI 问答（关于近期资讯） |

### 订阅接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/v1/subscriptions` | GET | 获取用户订阅 |
| `/api/v1/subscriptions` | POST | 创建订阅 |
| `/api/v1/subscriptions/{id}` | PUT | 更新订阅 |

### 管理接口

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/v1/admin/crawl` | POST | 手动触发爬虫 |
| `/api/v1/admin/process` | POST | 手动触发 AI 处理 |
| `/api/v1/admin/email` | POST | 发送精选邮件 |

### 请求示例

```bash
# 获取今日文章，按分类筛选
curl "https://api.ainewshub.dev/v1/articles/today?category=llm&min_score=70"

# 响应
{
  "data": [
    {
      "id": "abc123",
      "title": "GPT-5 发布：推理能力提升 300%",
      "summary": "OpenAI 发布 GPT-5，在推理能力上取得突破...",
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

## 质量评分算法

我们的透明评分系统帮助你识别最有价值的内容：

```
总分 = 来源权威度 (30%) 
     + 内容深度 (25%) 
     + 时效性 (20%) 
     + 社区信号 (15%) 
     + 原创性 (10%)

来源权威度:
  • 顶会论文 / 官方博客: 90-100
  • 主流科技媒体: 70-85  
  • 个人博客 / Twitter: 40-60（根据作者影响力调整）

内容深度:
  • 带代码的技术分析: 90-100
  • 详细解读: 70-85
  • 新闻摘要: 50-65
  • 简短提及: 30-45
```

## 配置说明

### 环境变量

| 变量 | 描述 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | PostgreSQL 连接字符串 | `postgresql://...` |
| `REDIS_URL` | Redis 连接字符串 | `redis://localhost:6379` |
| `OPENAI_API_KEY` | OpenAI API 密钥（用于摘要） | - |
| `ANTHROPIC_API_KEY` | Claude API 密钥（备选） | - |
| `JWT_SECRET` | JWT 令牌签名密钥 | - |
| `SMTP_HOST` | SMTP 服务器（邮件） | - |
| `SMTP_PORT` | SMTP 端口 | `587` |
| `SMTP_USER` | SMTP 用户名 | - |
| `SMTP_PASSWORD` | SMTP 密码 | - |
| `CRAWLER_INTERVAL` | 爬虫间隔（分钟） | `60` |

## 添加新数据源

通过实现 `BaseCrawler` 接口扩展爬虫系统：

```python
# backend/app/services/crawler/my_source.py
from .base import BaseCrawler, RawArticle

class MySourceCrawler(BaseCrawler):
    name = "my_source"
    base_url = "https://example.com"
    
    async def crawl(self) -> list[RawArticle]:
        # 实现你的爬取逻辑
        articles = []
        # ... 获取和解析文章
        return articles
```

在 `crawler_service.py` 中注册：

```python
from .crawler.my_source import MySourceCrawler

CRAWLERS = [
    ArxivCrawler(),
    TechCrunchCrawler(),
    MySourceCrawler(),  # 添加到这里
]
```

## 本地开发

### 环境要求

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- PostgreSQL 15+
- Redis 7+

### 运行测试

```bash
# 后端测试
cd backend
pytest --cov=app tests/

# 前端测试
cd frontend
npm test

# 端到端测试
npm run test:e2e
```

### 代码规范

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

## 开发路线图

### 已完成
- [x] 核心爬虫（arXiv、TechCrunch、The Verge）
- [x] AI 摘要 & 质量评分
- [x] Web 前端 MVP
- [x] 用户认证
- [x] 邮件订阅

### 进行中
- [ ] GitHub Trending 集成
- [ ] Twitter/X AI 大V 追踪
- [ ] 中文来源集成（机器之心等）

### 计划中
- [ ] 移动应用（React Native）
- [ ] 微信小程序
- [ ] 浏览器扩展
- [ ] Slack/Discord 机器人
- [ ] 向量搜索（语义查询）
- [ ] 多语言支持
- [ ] 高级功能 & API 分层

查看我们的 [公开路线图](https://github.com/ai-news/ai-news/projects/1) 了解详情。

## 参与贡献

我们欢迎贡献！在提交 Pull Request 之前，请先阅读我们的 [贡献指南](CONTRIBUTING.md)。

### 贡献方式

- **报告 Bug** — 提交 Issue 描述问题
- **建议功能** — 发起 Discussion 讨论新想法
- **提交 PR** — 修复 Bug 或实现功能
- **添加爬虫** — 集成新数据源
- **完善文档** — 修正错误或改进说明
- **翻译** — 帮助国际化

### 开发流程

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: 添加某个很棒的功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 发起 Pull Request

## 社区

- **Discord** — [加入 Discord 服务器](https://discord.gg/ainews) 参与讨论
- **Twitter** — 关注 [@ainewshub](https://twitter.com/ainewshub) 获取更新
- **GitHub Discussions** — [提问和讨论](https://github.com/ai-news/ai-news/discussions)
- **微信群** — 扫码加入微信交流群

## 安全

如果你发现安全漏洞，请发送邮件至 security@ainewshub.dev，请勿公开提交 Issue。

详细信息请参考 [SECURITY.md](SECURITY.md)。

## 许可证

本项目采用 **MIT 许可证** — 详见 [LICENSE](LICENSE) 文件。

## 致谢

- 灵感来源于 [Hacker News](https://news.ycombinator.com)、[TLDR AI](https://tldr.tech/ai) 和 [The Rundown AI](https://therundown.ai)
- 基于 [FastAPI](https://fastapi.tiangolo.com)、[Next.js](https://nextjs.org) 和 [Tailwind CSS](https://tailwindcss.com) 构建
- AI 能力由 [OpenAI](https://openai.com) 和 [Anthropic](https://anthropic.com) 提供
- 感谢所有 [贡献者](https://github.com/ai-news/ai-news/graphs/contributors)

---

<p align="center">
  <sub>由 AI News Hub 社区用 ❤️ 构建</sub>
</p>
