from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE


def build_database_prompt(category: Category, difficulty: Difficulty) -> str:

    return f"""
You are a Senior Software Engineer conducting a database interview.

Generate ONE realistic database interview question.

CATEGORY
- {category.value}

DIFFICULTY
- {difficulty.value}
- {DIFFICULTY_GUIDE[difficulty]}

Requirements:
- Match the requested difficulty.
- Focus on SQL, indexing, transactions, normalization, ACID, NoSQL, or query optimization.
- Ask exactly one question.

Answer Requirements:
- Explain the reasoning.
- Mention trade-offs when appropriate.
- Explain why the chosen approach works.
- No code.

Return ONLY valid JSON.

{{
    "question": "...",
    "answer": "...",
    "company": null,
    "tags": ["...", "...", "..."]
}}
"""