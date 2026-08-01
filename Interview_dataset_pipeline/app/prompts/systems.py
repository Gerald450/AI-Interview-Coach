from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE


def build_systems_prompt(category: Category, difficulty: Difficulty) -> str:
    return f"""
You are a Senior Software Engineer conducting a computer systems interview.

Generate ONE realistic interview question.

CATEGORY
- {category.value}

DIFFICULTY
- {difficulty.value}
- {DIFFICULTY_GUIDE[difficulty]}

Requirements:
- Match the requested difficulty.
- Focus on operating systems, networking, concurrency, or computer architecture.
- Ask exactly one question.

Answer Requirements:
- Explain the underlying concepts.
- Explain reasoning.
- Mention trade-offs only when relevant.
- No code.

Return ONLY valid JSON.

{{
    "question": "...",
    "answer": "...",
    "company": null,
    "tags": ["...", "...", "..."]
}}
"""