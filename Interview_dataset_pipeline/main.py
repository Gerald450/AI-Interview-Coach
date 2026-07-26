from turtle import towards
from app.models.interview import (
    InterviewExample,
    Difficulty,
    Category,
)
from app.generators.interview_generator import InterviewGenerator
from rich import print
from app.storage.jsonl_writer import JSONLWriter
from app.config import TARGET_DATASET_SIZE
import json
from pathlib import Path


def next_id(path: str) -> int:
    p = Path(path)
    if not p.exists():
        return 1
    last = None
    with p.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last = line
    return json.loads(last)["id"] + 1 if last else 1


dataset_path = "datasets/raw/interviews.jsonl"

CUSTOM_TARGET = 5

current_id = next_id(dataset_path)
generator = InterviewGenerator(current_id=current_id, max_retries=20)
writer = JSONLWriter(dataset_path)
result = generator.generate_random()


saved = 0

while saved < CUSTOM_TARGET:
    result = generator.generate_random()
    if writer.write(result):
        saved += 1
        print(f"Saved {saved}/{CUSTOM_TARGET}: id={result.id}")
        print("=" * 100)
print("Done!")
