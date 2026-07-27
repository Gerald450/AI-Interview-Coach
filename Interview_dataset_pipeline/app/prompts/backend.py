from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE


def build_backend_prompt(category: Category, difficulty: Difficulty) -> str:
    return f"""
You are a Senior Backend Software Engineer conducting an interview.

Generate ONE backend engineering interview question.

CATEGORY
- {category.value}

DIFFICULTY
- {difficulty.value}
- {DIFFICULTY_GUIDE[difficulty]}

Requirements:
- Match the requested difficulty.
- Focus on APIs, backend architecture, testing, or security.
- Ask exactly one question.

Answer Requirements:
- Explain the reasoning.
- Discuss best practices.
- Mention trade-offs only when appropriate.
- No code.

Return ONLY valid JSON.

{{
    "question": "...",
    "answer": "...",
    "company": null,
    "tags": ["...", "...", "..."]
}}
"""