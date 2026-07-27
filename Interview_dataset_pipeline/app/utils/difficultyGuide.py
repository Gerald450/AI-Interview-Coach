from app.models.interview import (
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