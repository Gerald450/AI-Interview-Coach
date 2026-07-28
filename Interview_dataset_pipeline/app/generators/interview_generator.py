import random
from datetime import datetime, timezone
from json import JSONDecodeError

from app.config import (
    CATEGORIES,
    DIFFICULTIES,
)
from app.generators.llm_client import LLMClient
from app.models.interview import Category, Difficulty, InterviewExample, JudgeExample
from app.prompts.judge import build_judge_prompt
from app.utils.qualityError import QualityError
from pydantic import ValidationError
from rich import print


class InterviewGenerator:
    def __init__(self, current_id: int = 1, max_retries: int = 5) -> None:
        self.client = LLMClient()
        self.current_id = current_id
        self.max_retries = max_retries

    def generate(
        self,
        category: Category,
        difficulty: Difficulty,
    ) -> InterviewExample:
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                data = self.client.generate(category=category, difficulty=difficulty)
                print(data)
                interview = InterviewExample(
                    id=self.current_id,
                    question=data["question"],
                    answer=data["answer"],
                    difficulty=difficulty,
                    category=category,
                    company=data.get("company"),
                    tags=data.get("tags", []),
                    created_at=datetime.now(timezone.utc),
                )
                # print("judging.....")
                # judge_data = self.client.judge(interview)

                # verdict = JudgeExample(
                #     Score=judge_data["Score"],
                #     Pass=judge_data["Pass"],
                #     Reason=judge_data["Reason"],
                # )

                # print("Verdict: ", verdict)

                # if not verdict.Pass or verdict.Score < 50:
                #     raise QualityError(verdict.Reason, verdict.Score)
                # print("done judging")
                # judge
                # get the score
                # if low score raise error
                self.current_id += 1

                return interview
            except (
                ValidationError,
                JSONDecodeError,
                KeyError,
                TypeError,
                QualityError,
            ) as error:
                last_error = error
                print(f"Attempt {attempt} failed {error}")
                print("=" * 100)
                continue

        raise RuntimeError(
            f"failed to generate valid InterviewExample after {self.max_retries} attempts"
        ) from last_error

    def generate_random(self) -> InterviewExample:
        return self.generate(
            category=random.choice(CATEGORIES),
            difficulty=random.choice(DIFFICULTIES),
        )
