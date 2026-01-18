import json
import httpx
from typing import Optional, Dict, Any
from app.config import settings
from app.models.article import ArticleCategory


class AIProcessor:
    """AI processing service for article summarization and quality scoring."""
    
    def __init__(self):
        self.openai_api_key = settings.OPENAI_API_KEY
        self.anthropic_api_key = settings.ANTHROPIC_API_KEY
    
    async def process_article(self, title: str, content: str, source: str) -> Dict[str, Any]:
        """Process an article: generate summary, translate, categorize, and score."""
        
        # If no API keys configured, use mock processing
        if not self.openai_api_key and not self.anthropic_api_key:
            return self._mock_process(title, content, source)
        
        try:
            if self.openai_api_key:
                return await self._process_with_openai(title, content, source)
            elif self.anthropic_api_key:
                return await self._process_with_anthropic(title, content, source)
        except Exception as e:
            print(f"AI processing error: {e}")
            return self._mock_process(title, content, source)
    
    async def _process_with_openai(self, title: str, content: str, source: str) -> Dict[str, Any]:
        """Process article using OpenAI API."""
        prompt = self._build_prompt(title, content, source)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You are an AI news analyst. Always respond in valid JSON format."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000,
                },
                timeout=60.0,
            )
            
            if response.status_code == 200:
                result = response.json()
                content_text = result["choices"][0]["message"]["content"]
                return self._parse_ai_response(content_text)
            else:
                return self._mock_process(title, content, source)
    
    async def _process_with_anthropic(self, title: str, content: str, source: str) -> Dict[str, Any]:
        """Process article using Anthropic API."""
        prompt = self._build_prompt(title, content, source)
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.anthropic_api_key,
                    "Content-Type": "application/json",
                    "anthropic-version": "2023-06-01",
                },
                json={
                    "model": "claude-3-haiku-20240307",
                    "max_tokens": 2000,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                },
                timeout=60.0,
            )
            
            if response.status_code == 200:
                result = response.json()
                content_text = result["content"][0]["text"]
                return self._parse_ai_response(content_text)
            else:
                return self._mock_process(title, content, source)
    
    def _build_prompt(self, title: str, content: str, source: str) -> str:
        """Build the prompt for AI processing."""
        # Truncate content if too long
        max_content_length = 8000
        if len(content) > max_content_length:
            content = content[:max_content_length] + "..."
        
        return f"""Analyze this AI-related article and provide:
1. A concise English summary (3 sentences: what it is, why it matters, what's the impact)
2. Chinese translation of the title
3. Chinese translation of the summary
4. Category classification
5. Quality scores

Article Title: {title}
Source: {source}
Content: {content}

Respond in this exact JSON format:
{{
    "summary": "3-sentence English summary here",
    "title_zh": "中文标题",
    "summary_zh": "三句话中文摘要",
    "category": "one of: llm, multimodal, agent, cv, nlp, rl, robotics, ai_safety, business, other",
    "tags": ["tag1", "tag2", "tag3"],
    "quality_score": 75,
    "content_depth": 70,
    "source_authority": 80
}}

Quality scoring guidelines (0-100):
- source_authority: Official blogs (90-100), Top media (70-85), Others (40-60)
- content_depth: Technical details, novelty, comprehensiveness
- quality_score: Overall weighted average"""
    
    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """Parse the AI response JSON."""
        try:
            # Try to extract JSON from the response
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        # Return default if parsing fails
        return self._default_result()
    
    def _mock_process(self, title: str, content: str, source: str) -> Dict[str, Any]:
        """Mock processing when no API key is configured."""
        # Simple keyword-based categorization
        title_lower = title.lower()
        content_lower = (content or "").lower()
        text = title_lower + " " + content_lower
        
        category = ArticleCategory.OTHER.value
        if any(kw in text for kw in ["gpt", "llm", "language model", "chatgpt", "claude"]):
            category = ArticleCategory.LLM.value
        elif any(kw in text for kw in ["multimodal", "vision-language", "image", "video"]):
            category = ArticleCategory.MULTIMODAL.value
        elif any(kw in text for kw in ["agent", "autonomous", "tool use"]):
            category = ArticleCategory.AGENT.value
        elif any(kw in text for kw in ["robot", "embodied", "manipulation"]):
            category = ArticleCategory.ROBOTICS.value
        
        # Source-based authority score
        source_scores = {
            "arxiv": 85,
            "openai_blog": 95,
            "google_ai_blog": 95,
            "meta_ai_blog": 90,
            "techcrunch": 70,
            "the_verge": 65,
            "jiqizhixin": 75,
        }
        source_authority = source_scores.get(source, 50)
        
        # Generate simple summary
        summary = f"This article discusses {title}. "
        if content:
            sentences = content.split('.')[:2]
            summary += '. '.join(s.strip() for s in sentences if s.strip()) + '.'
        
        return {
            "summary": summary[:500],
            "title_zh": f"[待翻译] {title}",
            "summary_zh": f"[待翻译] {summary[:200]}",
            "category": category,
            "tags": [],
            "quality_score": (source_authority * 0.4 + 60 * 0.6),
            "content_depth": 60,
            "source_authority": source_authority,
        }
    
    def _default_result(self) -> Dict[str, Any]:
        """Return default result on error."""
        return {
            "summary": "",
            "title_zh": "",
            "summary_zh": "",
            "category": ArticleCategory.OTHER.value,
            "tags": [],
            "quality_score": 50,
            "content_depth": 50,
            "source_authority": 50,
        }


# Singleton instance
ai_processor = AIProcessor()
