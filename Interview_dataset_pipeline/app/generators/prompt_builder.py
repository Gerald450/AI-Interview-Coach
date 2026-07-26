from app.models.interview import (
    Category,
    Difficulty,
)

DIFFICULTY_GUIDE = {
    Difficulty.EASY: (
        "A warm-up a competent junior answers in under a minute. "
        "Tests one core definition or a single well-known technique."
    ),
    Difficulty.MEDIUM: (
        "Requires connecting two or more ideas, or reasoning about a trade-off. "
        "Typical of a mid-level phone screen."
    ),
    Difficulty.HARD: (
        "Requires deep reasoning, edge cases, or scale and trade-off analysis. "
        "Typical of a senior on-site round."
    ),
}


class PromptBuilder:
    @staticmethod
    def build(
        category: Category,
        difficulty: Difficulty,
    ) -> str:
        return f"""
        You are a senior software engineer writing high-quality interview practice material.
        Write exactly ONE interview question and its model answer.
        TOPIC
        - Category: {category.value}
        - Difficulty: {difficulty.value} — {DIFFICULTY_GUIDE[difficulty]}
        QUESTION RULES
        - Phrase it as something an interviewer would actually say out loud, in full sentences.
        - Make it self-contained. No references to code, data, or context the candidate cannot see.
        - It must clearly belong to the {category.value} category.
        - Exactly one question. Do not bundle several questions together.
        ANSWER RULES
        - Answer the way a strong candidate would speak: 3 to 6 sentences, roughly 400-900 characters.
        - Explain the reasoning, not just the conclusion. Never reply with only a final value, a bare
        expression, a single word, or a fragment of code.
        - Name the key trade-off, complexity, or failure mode when the topic has one.
        - Plain prose only. No markdown, no bullet points, no code fences, no JSON, no wrapping quotes.
        - Describe code in words ("iterate once with a hash map") instead of pasting a program.
        TAG RULES
        - Exactly 3 to 5 tags, and never an empty list.
        - Lowercase, 1 to 3 words, hyphenated when multi-word: "hash-map", "time-complexity".
        - Name the concrete concepts the question tests. No filler like "interview", "question", "coding".
        - No duplicates and no near-duplicates of each other.
        COMPANY RULE
        - Use null unless the question is genuinely tied to one company's known interview style or product.
        - Null is correct the large majority of the time.
        OUTPUT
        Return ONLY a JSON object with exactly these four keys and nothing else:
        {{
        "question": "<string>",
        "answer": "<string>",
        "company": null,
        "tags": ["<string>", "<string>", "<string>"]
        }}
        Choose tags only after writing the question. Each tag must describe a concept actually tested by
        that specific question and must fit the requested {category.value} category.
        """
