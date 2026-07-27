from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE


def build_general_prompt(category: Category, difficulty: Difficulty) -> str:
    return f"""
You are a Senior Software Engineer conducting a technical interview.

Generate ONE realistic interview question.

CATEGORY
- {category.value}

DIFFICULTY
- {difficulty.value}
- {DIFFICULTY_GUIDE[difficulty]}

Requirements:
- Match the requested category.
- Match the requested difficulty.
- Ask exactly one question.
- Make the question realistic and technically accurate.

Answer Requirements:
- Fully answer the question.
- Explain the reasoning.
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