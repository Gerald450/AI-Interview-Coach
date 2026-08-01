import json
from pathlib import Path
from turtle import towards

from app.config import TARGET_DATASET_SIZE
from app.generators.interview_generator import InterviewGenerator
from app.models.interview import (
    Category,
    Difficulty,
    InterviewExample,
)
from app.storage.jsonl_writer import JSONLWriter
from rich import print


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


dataset_path = "datasets/raw/api_dataset.jsonl"


current_id = next_id(dataset_path)
CUSTOM_TARGET = 5000 - current_id
generator = InterviewGenerator(current_id=current_id, max_retries=20)
writer = JSONLWriter(dataset_path)


saved = 0

while saved < CUSTOM_TARGET:
    result = generator.generate_random()
    if writer.write(result):
        saved += 1
        print(f"Saved {saved}/{CUSTOM_TARGET}: id={result.id}")
        print("=" * 100)
print("Done!")
