import json
import os

from app.generators.prompt_builder import PromptBuilder
from app.models.interview import Category, Difficulty, InterviewExample
from app.prompts.judge import build_judge_prompt
from dotenv import load_dotenv
from google import genai
from groq import Groq
from rich import print

load_dotenv()


GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GROQ_API_KEY = os.environ["GROQ_API_KEY"]


class LLMClient:
    def __init__(self, model: str = "openai/gpt-oss-20b"):
        self.model = model
        self.client = Groq(api_key=GROQ_API_KEY)

    def generate(
        self,
        category: Category,
        difficulty: Difficulty,
    ) -> dict:

        prompt = PromptBuilder.build(category=category, difficulty=difficulty)

        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)

    def judge(self, interview: InterviewExample) -> dict:
        prompt = build_judge_prompt(
            interview.category,
            interview.difficulty,
            interview.question,
            interview.answer,
        )

        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)
