from app.models.interview import (
    Category,
    Difficulty,
)


def build_judge_prompt(category: Category, difficulty: Difficulty, generated_question: str, generated_answer: str) -> str:

    return f"""
    You are a senior software engineering interviewer reviewing interview questions for a training dataset.

    Your job is to determine whether the following interview question and answer are high enough quality to include in a fine-tuning dataset.

    Category:
    {category.value}

    Difficulty:
    {difficulty.value}

    Question:
    {generated_question}

    Answer:
    {generated_answer}

    Evaluate the example using these criteria.

    1. Technical correctness
    - Is the answer factually correct?
    - Are there any false claims?

    2. Category accuracy
    - Does the question clearly belong to the requested category?

    3. Interview realism
    - Does this sound like a real interview question asked by companies such as Google, Meta, Amazon, Microsoft, Stripe, Airbnb, Uber, or Datadog?

    4. Answer quality
    - Does the answer fully answer the question?
    - Is the reasoning correct?
    - Is the explanation clear?

    5. Hallucinations
    - Does the question invent unnecessary scenarios?
    - Does it misuse technical terminology?

    Return ONLY valid JSON.

    {{
        "Score": 0-100,
        "Pass": true,
        "Reason": "<short explanation>"
    }}
    """