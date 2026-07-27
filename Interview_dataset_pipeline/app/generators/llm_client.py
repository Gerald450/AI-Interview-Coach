import json
import ollama

from app.generators.prompt_builder import PromptBuilder
from app.models.interview import Category, Difficulty


class LLMClient:
    def __init__(self, model: str = "llama3.2:1b", prompt: str = ""):
        self.model = model
        self.prompt = prompt

    def generate(
        self,
        category: Category,
        difficulty: Difficulty,
    ) -> dict:
        if self.prompt:
            prompt = self.prompt
        else:
            prompt = PromptBuilder.build(category=category, difficulty=difficulty)

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            format="json",
        )

        return json.loads(response["message"]["content"])
