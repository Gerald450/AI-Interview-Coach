from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE


def build_programming_prompt(category: Category, difficulty: Difficulty) -> str:
    return f"""
You are a Senior Software Engineer conducting a programming fundamentals interview.

Generate ONE realistic interview question.

CATEGORY
- {category.value}

DIFFICULTY
- {difficulty.value}
- {DIFFICULTY_GUIDE[difficulty]}

Requirements:
- The question must clearly belong to {category.value}.
- Match the requested difficulty.
- Test understanding of programming concepts rather than memorization.
- Ask exactly one question.

Answer Requirements:
- Explain the underlying concept clearly.
- Use examples when appropriate.
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