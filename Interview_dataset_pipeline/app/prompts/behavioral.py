from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE


def build_behavioral_prompt(category: Category, difficulty: Difficulty) -> str:
    return f"""
You are a Senior Software Engineer conducting a behavioral interview.

Generate ONE realistic behavioral interview question.

CATEGORY
- {category.value}

DIFFICULTY
- {difficulty.value}
- {DIFFICULTY_GUIDE[difficulty]}

Requirements:
- The question should resemble interviews at Google, Amazon, Meta, Microsoft, Stripe, or Airbnb.
- The question must match the requested difficulty.
- Ask exactly one question.
- The question should assess communication, teamwork, ownership, leadership, conflict resolution, or decision-making.
- Do not combine multiple questions.

Answer Requirements:
- Answer using the STAR framework naturally.
- Explain the Situation, Task, Action, and Result.
- Demonstrate strong communication and reflection.
- Be concise but complete.

Return ONLY valid JSON.

{{
    "question": "...",
    "answer": "...",
    "company": null,
    "tags": ["...", "...", "..."]
}}
"""