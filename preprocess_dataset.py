# shuffle dataset
# split, train 90%, val 10%
# change format
"""
{
  "messages": [
    {
      "role": "user",
      "content": "Explain what an API endpoint is."
    },
    {
      "role": "assistant",
      "content": "An API endpoint is..."
    }
  ]
}
"""

# save train.jsonl, val.jsonl
import json
import random
from pathlib import Path

from rich import print

input_path = Path("Interview_dataset_pipeline/datasets/raw/api_dataset.jsonl")
output_dir = Path("Interview_dataset_pipeline/datasets/processed")
output_dir.mkdir(parents=True, exist_ok=True)

with open(input_path, encoding="utf-8") as f:
    records = [json.loads(line.strip()) for line in f]

random.seed(42)
random.shuffle(records)

split = int(len(records) * 0.9)
train, val = records[:split], records[split:]


def format_row(row: dict) -> dict:
    return {
        "messages": [
            {"role": "user", "content": row["question"]},
            {"role": "assistant", "content": row["answer"]},
        ]
    }


def write_jsonl(path: Path, rows: list[dict]) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            formatted_row = format_row(row)
            f.write(json.dumps(formatted_row, ensure_ascii=False) + "\n")


write_jsonl(Path(f"{output_dir}/train.jsonl"), train)
write_jsonl(Path(f"{output_dir}/val.jsonl"), val)
