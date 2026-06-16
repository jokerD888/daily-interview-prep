from abc import ABC, abstractmethod
import json
import httpx
from app.core.config import settings


class CardGeneratorABC(ABC):
    @abstractmethod
    async def generate_cards(self, text: str) -> list[dict]:
        """Return list of {question, answer, importance_score}"""
        ...


class DeepSeekGenerator(CardGeneratorABC):
    PROMPT = """你是一个面试八股文卡片生成器。请分析以下资料内容，生成10~20张记忆卡片。
每张卡片包含问题(question)和答案(answer)，并按面试提问频率给出重要性评分(importance_score, 1-5，5为最高频)。

请以JSON数组格式返回，不要包含任何其他文字：
[
  {"question": "...", "answer": "...", "importance_score": 3},
  ...
]

资料内容：
{text}"""

    async def generate_cards(self, text: str) -> list[dict]:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                f"{settings.DEEPSEEK_BASE_URL}/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": settings.AI_MODEL,
                    "messages": [{"role": "user", "content": self.PROMPT.format(text=text[:8000])}],
                    "temperature": 0.7,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            return self._parse_json(content)

    def _parse_json(self, content: str) -> list[dict]:
        content = content.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1])
        return json.loads(content)


def get_card_generator() -> CardGeneratorABC:
    return DeepSeekGenerator()
