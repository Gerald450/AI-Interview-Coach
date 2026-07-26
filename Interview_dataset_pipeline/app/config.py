from app.models.interview import Category, Difficulty

TARGET_DATASET_SIZE = 5000

CATEGORIES = list(Category)
DIFFICULTIES = list(Difficulty)

COMPANIES = [
     None,
    "Google",
    "Meta",
    "Amazon",
    "Microsoft",
    "Apple",
    "Netflix",
    "OpenAI",
    "Anthropic",
    "Stripe",
    "Databricks",
    "Cloudflare",
]

TAGS_PER_EXAMPLE = (2, 5)