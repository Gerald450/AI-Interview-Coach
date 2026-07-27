from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE


def build_ai_prompt(category: Category, difficulty: Difficulty) -> str:
    return f"""
You are a Senior AI Engineer conducting an interview.

Generate ONE realistic AI engineering interview question.

CATEGORY
- {category.value}

DIFFICULTY
- {difficulty.value}
- {DIFFICULTY_GUIDE[difficulty]}

Requirements:
- Match the requested difficulty.
- Focus on machine learning, deep learning, LLMs, RAG, embeddings, vector databases, prompt engineering, or model deployment.
- Ask exactly one question.

Answer Requirements:
- Be technically accurate.
- Explain the reasoning.
- Mention trade-offs when appropriate.
- No code.

Return ONLY valid JSON.

{{
    "question": "...",
    "answer": "...",
    "company": null,
    "tags": ["...", "...", "..."]
}}
"""