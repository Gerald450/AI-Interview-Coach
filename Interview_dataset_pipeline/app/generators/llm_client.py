import json
import os

from app.generators.prompt_builder import PromptBuilder
from app.models.interview import Category, Difficulty, InterviewExample
from app.prompts.judge import build_judge_prompt
from dotenv import load_dotenv
from google import genai

load_dotenv()


GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]


class LLMClient:
    def __init__(self, model: str = "gemini-3.6-flash"):
        self.model = model
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate(
        self,
        category: Category,
        difficulty: Difficulty,
    ) -> dict:

        prompt = PromptBuilder.build(category=category, difficulty=difficulty)

        response = self.client.models.generate_content(
            model=self.model,
            contents={"text": prompt},
            config={
                "temperature": 1,
                "top_k": 20,
                "top_p": 0.95,
            },
        )

        return json.loads(response.candidates[0].content.parts[0].text)

    def judge(self, interview: InterviewExample) -> dict:
        prompt = build_judge_prompt(
            interview.category,
            interview.difficulty,
            interview.question,
            interview.answer,
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents={"text": prompt},
            config={
                "temperature": 0,
                "top_k": 20,
                "top_p": 0.95,
            },
        )

        return json.loads(response.candidates[0].content.parts[0].text)
