#!/usr/bin/env python3
"""
Initialize database with sample data for testing.
Run: python scripts/init_db.py
"""

import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from datetime import datetime, timedelta
import random
from sqlalchemy import text
from app.database import engine, AsyncSessionLocal, Base
from app.models.article import Article, ArticleSource, ArticleCategory


SAMPLE_ARTICLES = [
    {
        "title": "GPT-5 Achieves Breakthrough in Complex Reasoning Tasks",
        "title_zh": "GPT-5在复杂推理任务上取得突破",
        "url": "https://openai.com/blog/gpt-5",
        "content": "OpenAI announces GPT-5, featuring significant improvements in mathematical reasoning, code generation, and multi-step problem solving. The model demonstrates a 40% improvement on graduate-level math problems.",
        "summary": "OpenAI releases GPT-5 with major advances in reasoning. The model shows 40% better performance on complex math tasks. This could revolutionize AI applications in education and research.",
        "summary_zh": "OpenAI发布GPT-5，在推理能力上取得重大进展。该模型在复杂数学任务上表现提升40%。这可能将彻底改变AI在教育和研究领域的应用。",
        "source": ArticleSource.OPENAI_BLOG,
        "category": ArticleCategory.LLM,
        "quality_score": 95,
        "source_authority": 98,
        "content_depth": 85,
        "authors": ["OpenAI Research Team"],
        "tags": ["GPT-5", "LLM", "reasoning", "OpenAI"],
    },
    {
        "title": "Attention Is All You Need: A New Efficient Transformer Architecture",
        "title_zh": "注意力即一切：一种新的高效Transformer架构",
        "url": "https://arxiv.org/abs/2401.12345",
        "content": "We propose a novel transformer architecture that reduces computational complexity from O(n²) to O(n log n) while maintaining model quality. Experiments show 3x speedup on long sequences.",
        "summary": "Researchers propose a more efficient transformer with O(n log n) complexity. The new architecture achieves 3x speedup on long sequences. This could enable processing of much longer documents.",
        "summary_zh": "研究人员提出了一种复杂度为O(n log n)的更高效Transformer。新架构在长序列上实现3倍加速。这可能使处理更长文档成为可能。",
        "source": ArticleSource.ARXIV,
        "category": ArticleCategory.LLM,
        "quality_score": 88,
        "source_authority": 85,
        "content_depth": 92,
        "authors": ["John Smith", "Jane Doe", "Bob Wilson"],
        "tags": ["transformer", "efficiency", "attention", "NLP"],
    },
    {
        "title": "Claude 4 Introduces Revolutionary Multi-Modal Capabilities",
        "title_zh": "Claude 4引入革命性的多模态能力",
        "url": "https://anthropic.com/blog/claude-4",
        "content": "Anthropic unveils Claude 4 with native support for images, audio, and video understanding. The model can now analyze complex visual scenes and generate detailed descriptions.",
        "summary": "Anthropic launches Claude 4 with true multi-modal understanding. The model processes images, audio, and video natively. This marks a significant step toward general AI assistants.",
        "summary_zh": "Anthropic推出具有真正多模态理解能力的Claude 4。该模型原生处理图像、音频和视频。这标志着向通用AI助手迈出了重要一步。",
        "source": ArticleSource.OTHER,
        "category": ArticleCategory.MULTIMODAL,
        "quality_score": 92,
        "source_authority": 90,
        "content_depth": 80,
        "authors": ["Anthropic Team"],
        "tags": ["Claude", "multimodal", "Anthropic", "AI assistant"],
    },
    {
        "title": "AutoGPT 2.0: Fully Autonomous AI Agents Are Here",
        "title_zh": "AutoGPT 2.0：完全自主的AI代理已到来",
        "url": "https://techcrunch.com/autogpt-2",
        "content": "The latest version of AutoGPT introduces persistent memory, tool use, and planning capabilities. Users report successful completion of complex multi-day tasks without human intervention.",
        "summary": "AutoGPT 2.0 brings persistent memory and advanced planning to AI agents. The system can now complete complex tasks over multiple days. This represents a major step toward autonomous AI.",
        "summary_zh": "AutoGPT 2.0为AI代理带来持久记忆和高级规划能力。该系统现在可以在多天内完成复杂任务。这代表着向自主AI迈出的重要一步。",
        "source": ArticleSource.TECHCRUNCH,
        "category": ArticleCategory.AGENT,
        "quality_score": 78,
        "source_authority": 70,
        "content_depth": 75,
        "authors": ["Sarah Connor"],
        "tags": ["AutoGPT", "agent", "autonomous", "AI"],
    },
    {
        "title": "Google DeepMind Achieves Human-Level Performance in Robot Manipulation",
        "title_zh": "Google DeepMind在机器人操作领域达到人类水平",
        "url": "https://deepmind.google/robot-learning",
        "content": "DeepMind's new RT-X model demonstrates unprecedented dexterity in robotic manipulation tasks. The system can tie shoelaces, fold clothes, and assemble furniture with 95% success rate.",
        "summary": "DeepMind's RT-X achieves 95% success in complex manipulation tasks. The robot can perform delicate tasks like tying shoelaces. This breakthrough could revolutionize robotics industry.",
        "summary_zh": "DeepMind的RT-X在复杂操作任务中达到95%成功率。该机器人可以执行系鞋带等精细任务。这一突破可能彻底改变机器人产业。",
        "source": ArticleSource.GOOGLE_AI_BLOG,
        "category": ArticleCategory.ROBOTICS,
        "quality_score": 90,
        "source_authority": 95,
        "content_depth": 88,
        "authors": ["DeepMind Robotics"],
        "tags": ["robotics", "manipulation", "DeepMind", "RT-X"],
    },
    {
        "title": "Vision Transformer Achieves New SOTA on ImageNet with 99.2% Accuracy",
        "title_zh": "Vision Transformer在ImageNet上达到99.2%准确率的新SOTA",
        "url": "https://arxiv.org/abs/2401.54321",
        "content": "A new vision transformer architecture sets record accuracy on ImageNet classification. The model uses sparse attention and achieves better results with fewer parameters.",
        "summary": "New ViT variant reaches 99.2% accuracy on ImageNet benchmark. The model uses sparse attention for efficiency. This pushes the boundaries of computer vision.",
        "summary_zh": "新的ViT变体在ImageNet基准上达到99.2%准确率。该模型使用稀疏注意力提高效率。这推动了计算机视觉的边界。",
        "source": ArticleSource.ARXIV,
        "category": ArticleCategory.CV,
        "quality_score": 85,
        "source_authority": 85,
        "content_depth": 90,
        "authors": ["Alice Zhang", "Bob Li"],
        "tags": ["ViT", "ImageNet", "computer vision", "SOTA"],
    },
    {
        "title": "Meta Releases Llama 4 with 1 Trillion Parameters",
        "title_zh": "Meta发布拥有1万亿参数的Llama 4",
        "url": "https://ai.meta.com/llama-4",
        "content": "Meta's Llama 4 is the largest open-source language model to date. The model is available for research and commercial use, with impressive benchmark results across various tasks.",
        "summary": "Meta launches Llama 4, an open-source model with 1T parameters. The model matches proprietary systems on most benchmarks. This democratizes access to cutting-edge AI.",
        "summary_zh": "Meta推出Llama 4，一个拥有1万亿参数的开源模型。该模型在大多数基准测试中与专有系统持平。这使得尖端AI技术更加普及。",
        "source": ArticleSource.META_AI_BLOG,
        "category": ArticleCategory.LLM,
        "quality_score": 93,
        "source_authority": 92,
        "content_depth": 82,
        "authors": ["Meta AI"],
        "tags": ["Llama", "open source", "Meta", "LLM"],
    },
    {
        "title": "AI Safety Researchers Propose New Alignment Framework",
        "title_zh": "AI安全研究人员提出新的对齐框架",
        "url": "https://arxiv.org/abs/2401.98765",
        "content": "A team of researchers introduces Constitutional AI 2.0, a framework for training AI systems that reliably follow human values. Early results show improved safety without sacrificing capability.",
        "summary": "New Constitutional AI 2.0 framework improves AI alignment. The method maintains capability while ensuring safety. This addresses key concerns in AI development.",
        "summary_zh": "新的Constitutional AI 2.0框架改善了AI对齐。该方法在确保安全的同时保持能力。这解决了AI开发中的关键问题。",
        "source": ArticleSource.ARXIV,
        "category": ArticleCategory.AI_SAFETY,
        "quality_score": 87,
        "source_authority": 85,
        "content_depth": 95,
        "authors": ["Safety Research Group"],
        "tags": ["AI safety", "alignment", "Constitutional AI"],
    },
    {
        "title": "Microsoft Copilot for Enterprise Reaches 100 Million Users",
        "title_zh": "Microsoft Copilot企业版用户突破1亿",
        "url": "https://theverge.com/microsoft-copilot-100m",
        "content": "Microsoft announces that its AI-powered Copilot assistant has reached 100 million enterprise users. Companies report 30% productivity gains on average.",
        "summary": "Microsoft Copilot hits 100M enterprise users milestone. Companies see 30% average productivity improvement. AI assistants are becoming essential workplace tools.",
        "summary_zh": "Microsoft Copilot企业用户达到1亿里程碑。企业平均生产力提升30%。AI助手正在成为必不可少的工作工具。",
        "source": ArticleSource.THE_VERGE,
        "category": ArticleCategory.BUSINESS,
        "quality_score": 72,
        "source_authority": 65,
        "content_depth": 60,
        "authors": ["Tech Reporter"],
        "tags": ["Microsoft", "Copilot", "enterprise", "productivity"],
    },
    {
        "title": "Reinforcement Learning Breakthrough: AI Masters StarCraft III",
        "title_zh": "强化学习突破：AI掌握星际争霸III",
        "url": "https://arxiv.org/abs/2401.11111",
        "content": "A new RL algorithm demonstrates superhuman performance in StarCraft III. The system learns complex strategies without human demonstrations using a novel hierarchical approach.",
        "summary": "New RL system achieves superhuman StarCraft III performance. The algorithm uses hierarchical learning without demonstrations. This advances our understanding of strategic AI.",
        "summary_zh": "新的强化学习系统在星际争霸III中达到超人类水平。该算法使用层次学习且无需示范。这推进了我们对战略AI的理解。",
        "source": ArticleSource.ARXIV,
        "category": ArticleCategory.RL,
        "quality_score": 83,
        "source_authority": 85,
        "content_depth": 88,
        "authors": ["RL Research Lab"],
        "tags": ["reinforcement learning", "StarCraft", "game AI"],
    },
]


async def init_db():
    """Initialize database with tables and sample data."""
    print("Creating database tables...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Tables created successfully!")
    
    async with AsyncSessionLocal() as session:
        # Check if data already exists
        result = await session.execute(text("SELECT COUNT(*) FROM articles"))
        count = result.scalar()
        
        if count > 0:
            print(f"Database already has {count} articles. Skipping sample data.")
            return
        
        print("Adding sample articles...")
        
        for i, article_data in enumerate(SAMPLE_ARTICLES):
            # Add some time variation
            days_ago = random.randint(0, 3)
            hours_ago = random.randint(0, 23)
            published_at = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)
            
            article = Article(
                title=article_data["title"],
                title_zh=article_data["title_zh"],
                url=article_data["url"],
                content=article_data["content"],
                summary=article_data["summary"],
                summary_zh=article_data["summary_zh"],
                source=article_data["source"],
                category=article_data["category"],
                quality_score=article_data["quality_score"],
                source_authority=article_data["source_authority"],
                content_depth=article_data["content_depth"],
                authors=article_data["authors"],
                tags=article_data["tags"],
                published_at=published_at,
                crawled_at=published_at + timedelta(minutes=30),
                processed_at=published_at + timedelta(hours=1),
                is_processed=1,
            )
            
            session.add(article)
            print(f"  Added: {article.title[:50]}...")
        
        await session.commit()
        print(f"\nSuccessfully added {len(SAMPLE_ARTICLES)} sample articles!")


if __name__ == "__main__":
    asyncio.run(init_db())
