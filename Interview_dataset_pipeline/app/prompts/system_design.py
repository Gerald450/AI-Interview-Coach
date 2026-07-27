from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE


def build_system_design_prompt(category: Category, difficulty: Difficulty) -> str:
    return f"""
You are a Senior Software Engineer conducting a system design interview.

Generate ONE realistic system design interview question.

CATEGORY
- {category.value}

DIFFICULTY
- {difficulty.value}
- {DIFFICULTY_GUIDE[difficulty]}

Requirements:
- Match the requested difficulty.
- Easy questions should focus on small systems.
- Medium questions should involve moderate scale and trade-offs.
- Hard questions should involve large-scale distributed systems.
- Ask exactly one question.

Answer Requirements:
- Explain the architecture.
- Discuss scalability.
- Discuss bottlenecks.
- Discuss trade-offs.
- Explain design decisions.
- No diagrams.

Return ONLY valid JSON.

{{
    "question": "...",
    "answer": "...",
    "company": null,
    "tags": ["...", "...", "..."]
}}
"""