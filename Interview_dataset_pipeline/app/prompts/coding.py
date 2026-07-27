from app.models.interview import (
    Category,
    Difficulty,
)
from app.utils.difficultyGuide import DIFFICULTY_GUIDE


def build_coding_prompt(category: Category, difficulty: Difficulty) -> str:

    return f"""
    You are a Senior Software Engineer conducting a coding interview.

    Generate ONE realistic interview question.

    CATEGORY
    - {category.value}

    DIFFICULTY
    - {difficulty.value}
    - {DIFFICULTY_GUIDE[difficulty]}

    Requirements:
    - The question should resemble interviews at Google, Meta, Amazon, Microsoft, Stripe, Uber, Airbnb, or Datadog.
    - The question must match the requested difficulty.
    - Focus on algorithmic problem solving.
    - Ask exactly one question.
    - Do not invent unnecessary business scenarios.
    - The problem should be solvable using concepts from {category.value}.
    - Do not mention the solution in the question.

    Answer Requirements:
    - Answer as an excellent candidate.
    - Explain the intuition first.
    - Explain the algorithm.
    - Mention time complexity.
    - Mention space complexity.
    - Mention important edge cases only when appropriate.
    - No code.
    - Natural interview-style explanation.

    Return ONLY valid JSON.

    {{
        "question": "...",
        "answer": "...",
        "company": null,
        "tags": ["...", "...", "..."]
    }}
    """