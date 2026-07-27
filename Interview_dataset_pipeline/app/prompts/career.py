from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE


def build_career_prompt(category: Category, difficulty: Difficulty) -> str:
    return f"""
You are a Senior Software Engineer helping candidates prepare for interviews.

Generate ONE realistic career-related interview question.

CATEGORY
- {category.value}

DIFFICULTY
- {difficulty.value}
- {DIFFICULTY_GUIDE[difficulty]}

Requirements:
- Match the requested difficulty.
- Focus on resumes, projects, internships, or career growth.
- Ask exactly one question.

Answer Requirements:
- Give practical, actionable advice.
- Explain the reasoning behind the advice.
- No bullet points.

Return ONLY valid JSON.

{{
    "question": "...",
    "answer": "...",
    "company": null,
    "tags": ["...", "...", "..."]
}}
"""