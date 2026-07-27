from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE


def build_cloud_prompt(category: Category, difficulty: Difficulty) -> str:
    return f"""
You are a Senior Cloud Engineer conducting an interview.

Generate ONE realistic cloud engineering interview question.

CATEGORY
- {category.value}

DIFFICULTY
- {difficulty.value}
- {DIFFICULTY_GUIDE[difficulty]}

Requirements:
- Match the requested difficulty.
- Focus on cloud infrastructure, containers, orchestration, CI/CD, monitoring, IAM, storage, networking, or serverless.
- Do not turn every question into full system design.
- Ask exactly one question.

Answer Requirements:
- Explain why the approach works.
- Mention trade-offs when relevant.
- No code.

Return ONLY valid JSON.

{{
    "question": "...",
    "answer": "...",
    "company": null,
    "tags": ["...", "...", "..."]
}}
"""