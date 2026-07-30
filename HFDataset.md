---
license: mit
task_categories:
  - text-generation
  - question-answering
language:
  - en
tags:
  - interview
  - software-engineering
  - chat
  - instruction-tuning
size_categories:
  - 1K<n<10K
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/train-*
      - split: validation
        path: data/validation-*
---

# Interview Coach Dataset

Chat-format dataset for fine-tuning an AI interview coach on software engineering interview Q&A.

## Dataset Summary

Each example is a single user/assistant turn in OpenAI-style `messages` format, suitable for instruction / chat fine-tuning (e.g. Unsloth, TRL, Hugging Face `SFTTrainer`).

- **Train:** ~1,017 examples
- **Validation:** ~114 examples
- **Total:** ~1,131 examples
- **Split:** 90% / 10% (seeded shuffle)

## Data Structure

```json
{
  "messages": [
    {"role": "user", "content": "...interview question..."},
    {"role": "assistant", "content": "...model answer..."}
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `messages` | list | Conversation turns |
| `messages[].role` | string | `"user"` or `"assistant"` |
| `messages[].content` | string | Question or answer text |

## Source

Derived from generated interview Q&A (`api_dataset.jsonl`), then shuffled, split, and reformatted for chat fine-tuning.

## Intended Use

Fine-tuning small/medium instruct models to practice answering technical interview questions (APIs, systems design, coding concepts, behavioral, etc.).

## Limitations

- Synthetic / generated content — may contain inaccuracies.
- English only.
- Coverage is uneven across topics and difficulty.
- Not a substitute for real interview feedback.

## Loading

```python
from datasets import load_dataset

ds = load_dataset("shimogerald/interview-coach-dataset")
print(ds["train"][0])
```
